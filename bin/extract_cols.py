#!/usr/bin/python
import sys, getopt
import os.path
import csv
from os import listdir

FIXED = ['seqNum', 'seqRNA']
COLUMNS = ['average_percentage_20',	'average_wout',	'average_percentage_70',	'average_percentage_50', 'average_out']

def usage():
    print 'extract_cols.py -d <directory>'

def find_csv_files(path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

def writeOutput(filename, header, data):
    outputfile = sys.stdout
    if filename != '':
        outputfile =  open(filename, 'w')

    csv_writer = csv.writer(outputfile, delimiter=";")
    if header != None:
        csv_writer.writerow(header)
    for row in data:
        csv_writer.writerow(row)

def main(argv):
    directory = ''
    outputfile = ''
    extension = '.csv';
    try:
        opts, args = getopt.getopt(argv,"hd:",["help","directory="])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-d", "--directory"):
            directory = arg
            print opt, arg
    outputfile = os.path.basename(os.path.normpath(directory))
    print "# Obtaining csv files from directory %s" % directory
    filenames = find_csv_files(directory)
    print "# Found %d files: %s" % (len(filenames), ", ".join(filenames))
    outputData = dict()
    # Read input files
    # We are loading all files data in memory so if the number of files is
    # high can use a lot of memory
    for filename in filenames:
        file_basename = os.path.splitext(os.path.basename(filename))[0]
        print file_basename
        input_file = os.path.join(directory, filename)
        print "# Processing file '%s'" % input_file
        # open the file in universal line ending mode
        with open(input_file, 'r') as infile:
          # read the file as a dictionary for each row ({header : value})
          reader = csv.DictReader(infile, delimiter=';')
          data = {}
          for row in reader:
            for header, value in row.items():
              try:
                data[header].append(value)
              except KeyError:
                data[header] = [value]

        for header_name in COLUMNS:
            if header_name in data:
                out_filename = header_name
                if not out_filename in outputData:
                    outputData[out_filename] = []
                for fixed_row in FIXED:
                    col = [file_basename + ' ' + fixed_row] + data[fixed_row]
                    outputData[out_filename].append(col)
                col_extra_header = [file_basename + ' ' + header_name] + data[header_name]
                outputData[out_filename].append(col_extra_header)

    for out_filename in outputData.keys():
        output_file_path = os.path.join(directory, out_filename) + extension
        print "# Writing file '%s'" % output_file_path
        data_to_write = zip(*outputData[out_filename])
        writeOutput(output_file_path, None, data_to_write)

if __name__ == "__main__":
    main(sys.argv[1:])
