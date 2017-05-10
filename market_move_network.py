#!/usr/bin/env python
from __future__ import print_function
import sys
import csv
import argparse
import json
from datetime import date, datetime, timedelta
from yahoo_finance import Share
 
def calculateRangeBased(symbol, days, base_num, base_type="percentage"):
    '''
    calculate range-based by points or percentages moved
    '''
    index = 0
    breached = 0
    dateTime = date.today()
    d = date.today() - timedelta(days=1835)
    stock = Share(symbol)
    jsonData = stock.get_historical(d.strftime("%Y-%m-%d"), date.today().strftime("%Y-%m-%d"))
    
    for item in jsonData[index:]:
        shift = index + days + 1
        newRows = jsonData[index:shift]
        try:
            startDate = newRows[0]["Date"]
            startDateClose = float(newRows[0]["Close"])
            endDate = newRows[days]["Date"]
            endDateClose = float(newRows[days]["Close"])
            move = endDateClose - startDateClose

            # Conversion to percentage or keep absolute value
            if base_type == "percentage":
                percentageChange = move / startDateClose * 100
                moveAbs = abs(percentageChange)
            else:
                moveAbs = abs(move)

        except IndexError:
            break

        if moveAbs >= base_num:
                breached = breached + 1
		if base_type == "percentage":
                	print("Start Date: %s, Start Date Close: %.2f, End Date: %s, End Date Close: %.2f, Move: %.2f, Percentage: %.2f%s" % (startDate, startDateClose, endDate, endDateClose, move, percentageChange, "%"))
		else:
                	print("Start Date: %s, Start Date Close: %.2f, End Date: %s, End Date Close: %.2f, Move: %.2f" % (startDate, startDateClose, endDate, endDateClose, move))
			
            # set pointer back to beginning of file
        index = index + 1

    percentageBreached = float(breached) / float(index) * 100
    print("Breached %d out of %d times: %.2f%s" % (breached, index, percentageBreached, "%"))

def main():
    '''
    main
    '''
    
    parser = argparse.ArgumentParser()
    #parser.add_argument("-i", "--input", action="store", default="spx_2010-2016_full.csv", metavar="csv", help="input CSV file from Yahoo Finance")
    parser.add_argument("-s", "--symbol", action="store", default="SPY", metavar="symbol", help="input symbol")
    parser.add_argument("-d", "--days", action="store", required=True, type=int, metavar="#", help="moving window of days")
    parser.add_argument("-p", "--percentage", action="store", type=float, metavar="%", help="use percentage move")
    parser.add_argument("-t", "--points", action="store", type=float, metavar="#", help="use points move")
    args = parser.parse_args()

    if not (args.percentage or args.points):
        parser.error('No range requested: add -p/--percentage or -t/--points')

    if args.percentage:
        calculateRangeBased(args.symbol, args.days, args.percentage, base_type="percentage")
    else:
        calculateRangeBased(args.symbol, args.days, args.points, base_type="points")
    

'''
send command-line arguments to main for processing
'''
if __name__ == "__main__":
    main()
