#!/usr/bin/python

import sys
import csv
from datetime import datetime
from datetime import timedelta

daysTotal = 0
percentage = 0
index = 0
breached = 0
'''
main
'''

# process command-line arguments
if len(sys.argv) < 3:
	print "ERROR: Must enter input file, days and percentage: ./market_percentage_move.py <input file> <days> <percentage>\nExample: ./market_percentage_move.py spx_2010-2016.csv 3 1"
	sys.exit()
else:
	filename = sys.argv[1]
	daysTotal = int(sys.argv[2])
	percentage = float(sys.argv[3])

with open(filename, 'rb') as f:
	reader = csv.reader(f)
	next(reader, None) # skip header 
	rows = list(reader)
	for row in rows[index:]:
		shift = index + daysTotal + 1
		newRows = rows[index:shift]
		try:
			startDate = newRows[0][0]
			startDateClose = float(newRows[0][4])
			endDate = newRows[daysTotal][0]
			endDateClose = float(newRows[daysTotal][4])
			move = endDateClose - startDateClose
			percentageChange = move / startDateClose * 100
			percentageChangeAbs = abs(percentageChange)
		except IndexError:
			break

		if percentageChangeAbs >= percentage:
			breached = breached + 1
			print "Start Date: %s, Start Date Close: %.2f, End Date: %s, End Date Close: %.2f, Move: %.2f, Percentage: %.2f" % (startDate, startDateClose, endDate, endDateClose, move, percentageChange)

		# set pointer back to beginning of file
		index = index + 1
	
	percentageBreached = float(breached) / float(index) * 100
	print "Breached %d out of %d times: %.2f%s" % (breached, index, percentageBreached, "%")
