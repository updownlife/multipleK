import os
import sys
import time
import timeit
from optparse import OptionParser

#Modify it to your working dir
# WORKING_DIR = "/home/stevenliu/workspace/multipleK/" # for old server
#WORKING_DIR = "/home/stevenliu/workspace/multipleK_paper_runing_human/multipleK/" # for new server
WORKING_DIR = "/home/stevenliu/big_disk/multipleK_paper_runing_human/multipleK/" # for new server
#WORKING_DIR = "/media/psf/Home/MultipleK/bin/multipleK/"
#read_file = WORKING_DIR + 'data/multipleK/SRR1798198.fastq'
#read_file = WORKING_DIR + 'data/multipleK/random_read.fastq'
#read_file = WORKING_DIR + 'data/multipleK/reads_ecoli.fasta'
read_file = WORKING_DIR + 'data/multipleK/read_CP65671.fasta '
kmer_file = WORKING_DIR + 'data/multipleK/kmer.fa'
query_file = WORKING_DIR + 'data/multipleK/boxquery'
result_file = WORKING_DIR + 'data/multipleK/result'

fast_format = 'fasta'

parser = OptionParser()
parser.add_option('-k','--klength', dest = "klength", help = "length of kmer")
parser.add_option('-s','--startk', dest = "startk", help = "minimum k")
parser.add_option('-e','--endk', dest = "endk", help = "maximum k")
parser.add_option('-q','--querynum', dest = "querynum", help = "number of query")
(options, args) = parser.parse_args(sys.argv[1:])

klength = options.klength
startk = int(options.startk)
endk = int(options.endk)
querynum = options.querynum

start = timeit.default_timer()

os.chdir(WORKING_DIR)

print "\n****** generate kmers from reads ******\n"
# fasta_fastkmer.py is for kmer list of fasta format
cmd = "python bin/reads2kmer/reads2kmer.py --output "+ kmer_file +" --klength "+ klength  +" --readsfile " + read_file + ' --format ' + fast_format
print "output kmer file: \n" + kmer_file
#print "sleep for 5 seconds..."
#time.sleep(5)
os.system(cmd)

print "\n****** compile bond-tree ******\n"
os.chdir(WORKING_DIR + 'src/')
# modify kmer length in code file dim.h and then compile bondtree
dim_file = open("dim.h", 'w')
dim_file.write("const int DIM = " + klength + ";")
dim_file.close()
os.system("make");

print "\n****** build index tree ******\n"
cmd = './ndTree --data '+ kmer_file + ' --mode rebuild ';
os.system(cmd)


print "\n****** multiple K query ******\n"
for i in range(startk, endk+1):
    print "\n******generate random box query******\n"
    os.chdir(WORKING_DIR)
    cmd = 'python bin/random_boxquery/random_fast_boxquery.py --num '+ querynum  +'  --klength '+ str(i) +' --output '+ query_file + str(i) +' --read '+ read_file +' --boxsize 1'+ ' --format '+ fast_format
    os.system(cmd)
    print "output query file: \n" + query_file + str(i)

    print "\n****** do box query k=" + klength + " K=" + str(i)
    os.chdir(WORKING_DIR + 'src/')
    cmd = 'python queryK.py -k '+ klength + ' -K '+ str(i) + ' -b ' + query_file + str(i) + ' -o '+ result_file + str(i)
    os.system(cmd)

    print "\n****** alignment ******\n"
    cmd = 'python ../bin/align_kmer_read/fast_align_kmer_read.py --readsfile ' + read_file + ' --resultsfile ' + result_file + str(i) + ' --queryfile ' + query_file + str(i) + ' --format ' + fast_format
    os.system(cmd)
    
    print "\n\n\n***** Done ******\n\n\n"

stop = timeit.default_timer()
print "***** running time *****\n"
print stop - start 
