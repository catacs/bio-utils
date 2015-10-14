#!/usr/bin/python
#
#./transformer.py input.csv transformations.csv > output.csv
##
#

# A Python program to read a csv file extract from a cell the content and replace
# elements with the tranformations rules.
# Program name - transformer.py
# Written by - Catalin Stanciu (catacsdev@gmail.com)
#
# Example:
#   transformer.py input.csv transformations.csv > output.csv
#
#
import sys
import os.path

toDelete = ['100b', '108b', '10b', '117b', '46', '49', '57', '62','75', '76']

toStart = 3
toEnd = 26

def readTranform(inputFile = None):
	transforms = {}
	if inputFile is None:
		return 1, "File not specified"
	elif not os.path.exists(inputFile):
		return 2, "Invalid file " + inputFile
	else:
		inputFile
		lines = [line.rstrip('\r\n') for line in open(inputFile)]
		lines.pop(0)
		for line in lines:
			parsed = [r.strip() for r in line.split(";")]
			if len(parsed) >= 3:
				transforms[parsed[1]] = parsed [3]
		return 0, transforms

def readData(inputFile):
	data = []
	if inputFile is None:
		return 1, "File not specified"
	elif not os.path.exists(inputFile):
		return 2, "Invalid file " + inputFile
	else:
		inputFile
		lines = [line.rstrip('\r\n') for line in open(inputFile)]
		for line in lines:
			parsed = [r.strip() for r in line.split(";")]
			data.append([r.strip() for r in parsed[2].split(",")])
		return 0, data

def applyTranformation(transforms, data):
	rows = []
	cols = []
	for line in data:
		cols =  []
		for v in line:
			if v not in toDelete:
				if v in transforms:
					cols.append(transforms[v])
				else:
					cols.append(v)
		rows.append(cols)
	return rows

def showExisting(transforms, data):
	result = [];
	mySet = set(reduce(lambda x,y: x.extend(y) or x, data))

	for  l in mySet:
		if l in transforms:
			 result.append(l + "   SI")
		else:
			result.append(l + "    NO")

	print "\r\n".join(sorted(result,key=lambda x:(str.lower(x),x)))

def writeOutput(data, mustSort=True):
	rows = []
	cols = ""
	index = 0;
	test = 0;
	for i in range(len(data)):
		setCount = ""
		vi = i-3
		sort = data[i]
		test = 0
		if vi > 0 and vi % 2 == 1:
			setCount = len(set(data[i]) &  set(data[i-1]))
		if mustSort and len(data[i]) >  1:
			sort.sort(key=int)
		if len(sort) != len(set(sort)):
			test = 1
		rows.append(",".join(sort) + "; " + str(len(data[i])) + ";" + str(setCount) + " ;" + str(test))
	return "\r\n".join(rows)

def removeInvalid(data):
	rows = []
	cols = []
	for line in data:
		cols =  []
		for v in line:
			if v not in toDelete:
				cols.append(v)
		rows.append(cols)
	return rows


def main(argv=None):
	if len(sys.argv) >= 2:
		inputFile = sys.argv[1]
		transformationsFile = sys.argv[2]
		err, transforms = readTranform(transformationsFile)
		if err > 0:
			print transforms
			return 1
		err, data = readData(inputFile)

		if err > 0:
			print data
			return 1
		# TODO  call to showExisting(transforms, data)
		output = applyTranformation(transforms,data)
		print writeOutput(removeInvalid(data), False)
		print writeOutput(output)

if __name__ == "__main__":
    sys.exit(main())
