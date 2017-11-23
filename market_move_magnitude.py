#!/usr/bin/env python
from __future__ import print_function
import sys
import csv
import argparse
from datetime import datetime
from datetime import timedelta

def calculateRangeBasedMagnitude(filename, days, multiplier):
    '''
    calculate range-based by points or percentages moved
    '''
    index = 0
    breached = 0
    currentPrice = 0
    counter = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        rows = list(reader)
        for row in rows[counter:]:
            currentPrice = float(rows[counter][4])
            counter = counter + 1
            index = counter
            shift = index + days
            for row in rows[index:shift]:
                index = index + 1
                try:
                    startDate = rows[counter][0]
                    startDateClose = float(rows[counter][4])
                    endDate = rows[index][0]
                    endDateClose = float(rows[index][4])
                    move = endDateClose - startDateClose

                    if(move > 0 and move >= ((currentPrice * multiplier) - currentPrice)):
                        print("Start Date: %s, Start Date Close: %.2f, End Date: %s, End Date Close: %.2f, Move: %.2f" % (startDate, startDateClose, endDate, endDateClose, move))
                        breached = breached + 1
                except IndexError:
                    break

        percentageBreached = float(breached) / counter * 100
        print("Breached: %d out of %d (%.2f%s)" % (breached, counter, percentageBreached, "%"))

def calculateMagnitude(filename):
    '''
    calculate single-day largest moves
    '''
    index = 0
    largestMove = 0
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        rows = list(reader)
        for row in rows[0:]:
            try:
                move = float(rows[index+1][2]) - float(rows[index][3])
                if move > largestMove:
                    largestMove = move
                    startDate = rows[index][0]
                    startDateLow = float(rows[index][3])
                    endDate = rows[index+1][0]
                    endDateHigh = float(rows[index+1][2])
                index = index + 1
            except IndexError:
                break

        print("Largest Move: %.2f\tStart Date: %s\tStart Date Low: %.2f\tEnd Date: %s\tEnd Date High: %.2f" % (largestMove, startDate, startDateLow, endDate, endDateHigh))

def main():
    '''
    main
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", action="store", default="vix_1999-2017.csv", metavar="csv", help="input CSV file from Yahoo Finance")
    parser.add_argument("-d", "--days", action="store", required=False, type=int, metavar="#", help="moving window of days")
    parser.add_argument("-m", "--multiplier", action="store", required=False, type=float, metavar="#", help="multipy by current price to get magnitude of move")
    args = parser.parse_args()

    if args.multiplier:
        calculateRangeBasedMagnitude(args.input, args.days, args.multiplier)
    else:
        calculateMagnitude(args.input)

'''
send command-line arguments to main for processing
'''
if __name__ == "__main__":
    main()
