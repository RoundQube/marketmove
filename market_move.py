#!/usr/bin/env python
from __future__ import print_function
import sys
import csv
import argparse
from datetime import datetime
from datetime import timedelta


def calculateRangeBased(filename, days, base_num, base_type="percentage"):
    '''
    calculate range-based by points or percentages moved
    '''
    index = 0
    breached = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        rows = list(reader)
        rows.reverse()
        for row in rows[index:]:
            shift = index + days + 1
            newRows = rows[index:shift]
            try:
                startDate = newRows[0][0]
                startDateClose = float(newRows[0][4])
                endDate = newRows[days][0]
                endDateClose = float(newRows[days][4])
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
    parser.add_argument("-i", "--input", action="store", default="spx_2010-2016_full.csv", metavar="csv", help="input CSV file from Yahoo Finance")
    parser.add_argument("-d", "--days", action="store", required=True, type=int, metavar="#", help="moving window of days")
    parser.add_argument("-p", "--percentage", action="store", type=float, metavar="%", help="use percentage move")
    parser.add_argument("-t", "--points", action="store", type=float, metavar="#", help="use points move")
    args = parser.parse_args()

    if not (args.percentage or args.points):
        parser.error('No range requested: add -p/--percentage or -t/--points')

    if args.percentage:
        calculateRangeBased(args.input, args.days, args.percentage, base_type="percentage")
    else:
        calculateRangeBased(args.input, args.days, args.points, base_type="points")


'''
send command-line arguments to main for processing
'''
if __name__ == "__main__":
    main()
