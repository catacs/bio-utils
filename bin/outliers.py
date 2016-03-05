#!/usr/bin/python
import sys, getopt
import os.path
import math
import numpy
import csv

HEADERS = ['seqNum', 'seqRNA', 'areaDiff', 'normDiff']

# def parse_float(string):
#     try:
#         return float(string)
#     except Exception:
#         throw TypeError

def try_parse_float(string, fail=None):
    try:
        return float(string)
    except Exception:
        return fail;

def usage():
    print 'outlyers.py -i <inputfile> [-o <outputfile>]'

def average_percentage(l, out, percentage, percentage_outlier):
    ordered = sorted(l, reverse=True)
    outliers = [x for x in ordered if x > out]
    out_percentage_length = int(math.ceil((len(outliers) * percentage_outlier) / 100.0))
    wout = ordered[out_percentage_length:]
    percentage_length = int(math.ceil(len(l) * percentage / 100.0))
    return average(wout[:percentage_length])

def average(l):
    length = len(l)
    if length > 0:
        return sum(l)/len(l)
    return 0

def average_out(l, out, percentage):
    ordered = sorted(l, reverse=True)
    length = int(math.ceil(len(l) * percentage / 100.0))
    return average(ordered[:length])

def average_wout(l, out, percentage):
    ordered = sorted(l, reverse=True)
    outliers = [x for x in ordered if x > out]
    out_length = len(outliers)
    wout = ordered[out_length:]
    length = int(math.ceil(len(l) * percentage / 100.0))
    return average(wout[:length])

def out(itr):
    return itr + (itr * 1.5)

def itr(q_1, q_3):
    return q_3 - q_1

def q1(l):
    positive_nums = [x for x in l if x >= 0]
    sorted_nums = sorted(positive_nums)
    low_mid = int(round( (len(sorted_nums) + 1 )  / 4.0 ) - 1 )
    lq = sorted_nums[low_mid]
    return lq

# First quartile of positive data
def q3(l):
    uq = 0;
    l = [x for x in l if x >= 0]
    positiveNums = sorted(l) #< Sort the list in ascending order
    try:
        high_mid = ( len( positiveNums ) - 1 ) * 0.75
        uq = positiveNums[ high_mid ]
    except TypeError:   #<  There were an even amount of values
        # Make sure to type results of math.floor/ceil to int for use in list indices
        ceil = int( math.ceil( high_mid ) )
        floor = int( math.floor( high_mid ) )
        uq = ( positiveNums[ ceil ] + positiveNums[ floor ] ) / 2

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
        original_header = lines[0].split()
        original_data = lines[1:]
        rows_to_process = [k for k in range(len(original_header)) if original_header[k] in HEADERS]

        header = [original_header[x] for x in rows_to_process]
        for cols in header:
            data.append([])

        for line in original_data:
            row = line.split()
            i = 0
            for col in rows_to_process:
                data[i].append(try_parse_float(row[col], row[col]))
                i += 1
    return header, data

def writeOutput(filename, header, table):
    csv.writer(sys.stdout)
    outputfile = sys.stdout
    if filename != '':
        outputfile =  open(filename, 'w')

    csv_writer = csv.writer(outputfile)
    csv_writer.writerow(header)
    for row in table:
        csv_writer.writerow(row)

def processData(header, table):
    percentage = 10
    processed_header = header
    processed_table = table
    area_diff_list = table[header.index('areaDiff')];
    param = dict()
    param_list = dict()

    # Calculate parameters
    param['q1'] = q1(area_diff_list)
    param['q3'] = q3(area_diff_list)
    param['itr'] = itr(param['q1'], param['q3'])
    param['out'] = out(param['itr'])
    param_list['average_out'] = average_out(area_diff_list, param['out'], percentage)
    param_list['average_wout'] = average_wout(area_diff_list, param['out'], percentage)
    param_list['average_percentage_50'] = average_percentage(area_diff_list, param['out'], percentage, 50)
    param_list['average_percentage_20'] = average_percentage(area_diff_list, param['out'], percentage, 20)
    param_list['average_percentage_70'] = average_percentage(area_diff_list, param['out'], percentage, 70)

    # Calculate new columns
    for (k, v) in param_list.items():
        processed_header.append(k)
        new_col = [bound_range(x/v, 0, 3) for x in area_diff_list]
        processed_table.append(new_col)
    return processed_header, processed_table, param, param_list

def main(argv):
    data = ''
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:w:s:o:",["help","inputfile=","outputfile=","window=","step="])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
    if os.path.isfile(inputfile):
        header, table = readInput(inputfile)
    else:
        print "Invalid input file '%s'." % inputfile
        usage()
        sys.exit(2)

    header, outputTable, param, param_list = processData(header, table)
    data_to_write = zip(*outputTable)
    writeOutput(outputfile, header, data_to_write)

if __name__ == "__main__":
    main(sys.argv[1:])
