#!/usr/bin/python
import sys, getopt
import os.path

def usage():
    print 'outlyers.py -i <inputfile> [-o <outputfile>]'
    sys.exit(2)

def averagePercentage(l, out, percentage, percentageOutlier):
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
    outSize = outliers.length
    wout = l[outSize:]
    size = int(round(len(ordered) * percentage) + 1)
    return average(wout[:size])

def out(itr):
    return itr + (itr * 1.5)

def itr(q1, q3):
    return q3 -q1

def q1(l):
    l = [x for x in nums if x >= 0]
    positiveNums = l.sort() #< Sort the list in ascending order
    low_mid = int( round( ( len(positiveNums) + 1 ) / 4.0 ) – 1 ) #< Thanks @Alex (comments)
    lq = positiveNums[low_mid]
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
        with open(inputfile) as f:
            data = f.read().splitlines()
            data = "".join(content)
    else:
        print "Invalid input file '%s'." % inputfile
        usage()
    options.append("# Input file is " +  inputfile)
    options.append("# Output file is " + outputfile)

    if outputfile != '':
        outfile = open(outputfile,'w')
            outfile.write("Test %s\n" % outputfile)
        outfile.close()
    else:
        print l


if __name__ == "__main__":
    main(sys.argv[1:])
