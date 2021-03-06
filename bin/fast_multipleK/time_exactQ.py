#!/usr/bin/env python
import os
import sys
import time
import timeit
from optparse import OptionParser

readFilename = "read_CP65671.fasta"
#readFilename = "read_NC32798.fasta"
#readFilename = "homo_read.fastq"
#readFilename = "random_read.fastq"
#readFilename = "reads_ecoli.fasta"
klength = 12
<<<<<<< HEAD
startk = 7
endk = 11
querynum = 1000
=======
startk = 6
endk = 11
querynum = 100
>>>>>>> 369cfeebd0116a46c7ea0939fd706786c002555d

patternId = '0'
WORKING_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),"../../")
read_file = WORKING_DIR + 'data/multipleK/' + readFilename
query_file = WORKING_DIR + 'data/multipleK/boxquery'
result_file = WORKING_DIR + 'data/multipleK/result'

print "\n****** compile bond-tree ******\n"
os.chdir(WORKING_DIR + 'src/')
# modify kmer length in code file dim.h and then compile bondtree
dim_file = open("dim.h", 'w')
dim_file.write("const int DIM = %s ;" % klength)
dim_file.close()
os.system("make");

for i in range(startk, endk+1):
    os.chdir(WORKING_DIR)
    cmd = 'python bin/random_boxquery/random_fast_boxquery.py --num '+ str(querynum)  +'  --klength '+ str(i) +' --output '+ query_file + str(i) +' --read '+ read_file +' --boxsize 1 --pattern ' + patternId 
    os.system(cmd)
    os.chdir(WORKING_DIR + 'src/')
    
    # Full box
    cmd = 'python exactQueryK.py -k '+ str(klength) + ' -K '+ str(i) + ' -b ' + query_file + str(i) + ' -o '+ result_file + str(i) + ' -t -1'
    os.system(cmd)

    # Full exact
    cmd = 'python exactQueryK.py -k '+ str(klength) + ' -K '+ str(i) + ' -b ' + query_file + str(i) + ' -o '+ result_file + str(i) + ' -t -1 --mode exact'
    os.system(cmd)

'''
    cmd = 'python ../bin/align_kmer_read/fast_align_kmer_read.py --readsfile ' + read_file + ' --resultsfile ' + result_file + str(i) + ' --queryfile ' + query_file + str(i) 
    os.system(cmd)
'''
