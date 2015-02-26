# Bio-Utils
This repository is intended to be a library with scripts utils for bioinformatic analysis.

## seqTokenizer:
seqTokenizer: read from a file all lines removing newline character. It gets segments from input with the window size. The step between 2 sequences is defined by step value.

Example:

inputfile content : ATGCATGCATGCATGCATGC

`seqTokenizer -i inputfile -o  outputfile -w 10 -s 2`

output:

 * ATGCATGCAT --> (0:9)
 * GCATGCATGC --> (2:11)
 * ATGCATGCAT --> (4:13)
 * GCATGCATGC --> (6:15)
 * ATGCATGCAT --> (8:17)
 * GCATGCATGC --> (10:19)
  
  
