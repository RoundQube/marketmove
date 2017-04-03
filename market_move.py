#!/usr/bin/python

import sys
import csv
import getopt
from datetime import datetime
from datetime import timedelta

'''
show error
'''
def showUsage():
	print "ERROR: Must enter input file, days and percentage (or points): ./market_move.py -i <input file> -d <days> -p <percentage> or -t <points>\nExample (percentage moved): ./market_move.py -i spx_2010-2016.csv -d 3 -p 1\nExample (points moved): ./market_move.py -i spx_2010-2016.csv -d 3 -t 25"
	sys.exit(2)

'''
calculate range-based by points moved
'''
def calculateRangeBasedPoints(filename, days, points):
	index = 0
	breached = 0
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		next(reader, None) # skip header 
		rows = list(reader) # 
		for row in rows[index:]:
			shift = index + days + 1
			newRows = rows[index:shift]
			try:
				startDate = newRows[0][0]
				startDateClose = float(newRows[0][4])
				endDate = newRows[days][0]
				endDateClose = float(newRows[days][4])
				move = endDateClose - startDateClose
				moveAbs = abs(move)
			except IndexError:
				break

			if moveAbs >= points:
				breached = breached + 1
				print "Start Date: %s, Start Date Close: %.2f, End Date: %s, End Date Close: %.2f, Move: %.2f" % (startDate, startDateClose, endDate, endDateClose, move)

			# set pointer back to beginning of file
			index = index + 1
	
		percentageBreached = float(breached) / float(index) * 100
		print "Breached %d out of %d times: %.2f%s" % (breached, index, percentageBreached, "%")

'''
calculate range-based by percentage moved
'''
def calculateRangeBasedPercentage(filename, days, percentage):
	index = 0
	breached = 0
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		next(reader, None) # skip header 
		rows = list(reader) # 
		for row in rows[index:]:
			shift = index + days + 1
			newRows = rows[index:shift]
			try:
				startDate = newRows[0][0]
				startDateClose = float(newRows[0][4])
				endDate = newRows[days][0]
				endDateClose = float(newRows[days][4])
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

'''
main
'''
def main(argv):
	
	byPercentage = True
	filename = ""
	days = 0
	percentage = 0
	points = 0

	try:
		opts, args = getopt.getopt(argv, "h:i:d:p:t:")
	except getopt.GetoptError:
		showUsage()

	for opt, arg in opts:
		if opt == '-h':
			showUsage()
		elif opt == '-i':
			filename = arg
		elif opt == '-d':
			days = int(arg)
		elif opt == '-p':
			percentage = float(arg)
			byPercentage = True
			byPoints = False
		elif opt == '-t':
			points = int(arg)
			byPercentage = False
			byPoints = True

	if byPercentage == True:
		calculateRangeBasedPercentage(filename, days, percentage)
	else:
		calculateRangeBasedPoints(filename, days, points)

	
'''
send command-line arguments to main for processing
'''
if __name__ == "__main__":
	main(sys.argv[1:])
