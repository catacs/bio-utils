#!/usr/bin/python
import sys, getopt
import os.path

HEADERS = ['seqNum', 'seqRNA', 'areaDiff', 'normDiff']

def usage():
    print 'outlyers.py -i <inputfile> [-o <outputfile>]'

def average_percentage(l, out, percentage, percentageOutlier):
    outliers = [x for x in l if x > out]
    outPSize = int(round(len(outliers) * percentageOutlier) + 1)
    wout = l[outPSize:]
    size = int(round(len(ordered) * percentage) + 1)
    return average(wout[:size])

def average(l):
    return sum(l)/len(l)

def average_out(l, out, percentage):
    ordered = l.sort()
    size = int(round(len(ordered) * percentage) + 1)
    return average(ordered[:size])

def average_wout(l, out, percentage):
    outliers = [x for x in l if x > out]
    out_size = outliers.length
    wout = l[out_size:]
    size = int(round(len(ordered) * percentage) + 1)
    return average(wout[:size])

def out(itr):
    return itr + (itr * 1.5)

def itr(q1, q3):
    return q3 -q1

def q1(l):
    l = [x for x in nums if x >= 0]
    positive_nums = l.sort() #< Sort the list in ascending order
    low_mid = int( round( ( len(positive_nums) + 1 ) / 4.0 ) – 1 ) #< Thanks @Alex (comments)
    lq = positive_nums[low_mid]
    return lq

# First quartile of positive data
def q3(l):
    uq = 0;
    l = [x for x in l if x >= 0]
    positiveNums = l.sort() #< Sort the list in ascending order
    try:
        high_mid = ( len( positiveNums ) - 1 ) * 0.75
        uq = positiveNums[ high_mid ]
    except TypeError:   #<  There were an even amount of values
        # Make sure to type results of math.floor/ceil to int for use in list indices
        ceil = int( math.ceil( high_mid ) )
        floor = int( math.floor( high_mid ) )
        uq = ( positiveNums[ ceil ] + positiveNums[ floor ] ) /

    return uq

def bound_range(v, ll, ul):
    if v < ll:
        return ll
    if v > ul:
        return ul
    return v
def readInput(filename):
    header = []
    data  = []
    with open(filename) as inputfile:
        lines = inputfile.read().splitlines()
        original_header = lines[1].split()
        original_data = lines[1:]
        rows_to_process = [k for (k, v) in original_header if v in HEADERS]

        header = [original_data(x) for x in rows_to_process]
        for cols in header:
            data.append([])

        for line in original_data:
            row = line.split()
            i = 0
            for col in rows_to_process:
                data[i].append(row[col])
                ++i

    return header, data

def writeOutput(filename, header, table):
    csv.writer(sys.stdout)
    outputfile = sys.stdout
    if filename == '':
        outputfile =  open(filename, 'w')

    csv_writer = csv.writer(outputfile)
    csv_writer.writerow(header)
    for row in range(len(table)):
        csv_writer.writerow(row)

def processData(header, table):
    percentage = 10
    processed_header = header
    processed_table = table
    area_diff_list = table[header.index('areaDiff')];
    param = dict()
    param_list = dict[]

    # Calculate parameters
    param['q1'] = q1(area_diff_list)
    param['q3' = q3(area_diff_list)
    param['itr'] = itr(q1, q3)
    param['out'] = out(itr)
    param_list['average_out'] = average_out(area_diff_list, out, percentage)
    param_list['average_wout'] = average_wout(area_diff_list, out, percentage)
    param_list['average_percentage_50'] = average_percentage(area_diff_list, out, percentage, 50)
    param_list['average_percentage_20'] = average_percentage(area_diff_list, out, percentage, 80)
    param_list['average_percentage_70'] = average_percentage(area_diff_list, out, percentage, 30)

    # Calculate new columns
    for (k, v) in param_list:
        processed_header.append(k)
        processed_table.append(bound_range(x/v) in area_diff_list)

    return processed_header, processed_table, param, param_list

def main(argv):
    data = ''
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:w:s:o:",["help","inputfile=","outputfile=","window=","step="])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        print "reading opt %s %s" % (opt,arg)
        if opt == '-h':
            usage()
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
    print inputfile
    if os.path.isfile(inputfile):
        header, table = readInput(inputfile)
    else:
        print "Invalid input file '%s'." % inputfile
        usage()
        sys.exit(2)


    header, outputTable = processData(header, table)
    data_to_write = zip(*outputTable)

    writeOutput(outfile, header, data_to_write)



if __name__ == "__main__":
    main(sys.argv[1:])
