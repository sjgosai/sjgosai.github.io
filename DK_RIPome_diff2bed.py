#! /usr/bin/python2.7

# This script will convert *.diff files generated by David Kelly
# for the RIPome project to *.bed files. These BED files can be
# visualized using custom tracks on the UCSC genome browser.
# Recommended inputs found in:
# /n/rinn_data1/users/dkelley/ripome/data/rips_final/

import sys
import subprocess

def ucsc_header():
	header_line = 'browser position chrX:130836678-130964671' + '\n'
	header_line += 'track name=RIPome visibility=2 '
	header_line += 'description="RIP peaks identified by DK" color=0,0,0,'
	return(header_line)

def main(in_file,out_file):
	open_file = open(in_file,'r')
	open_out = open(out_file,'w')
	track_header = ucsc_header()
	open_out.write(track_header + "\n")
	header = open_file.readline()
	l2fc_max = 0.0
	for line in open_file:
		line_split = line.rstrip().split("\t")
		locus = line_split[3]
		sample_1 = line_split[4]
		sample_2 = line_split[5]
		test_status = line_split[6]
		l2fc = line_split[9] 
		q_value = line_split[12]
		flag = line_split[13]
		(chrom,interval) = locus.split(":")
		(start,end) = interval.split("-")
		if sample_2 == 'input': # Cuffdiff l2fc based on sample_2/sample_1
			antibody = sample_1
			l2fc =  str( -1 * float(l2fc) )
		else:
			antibody = sample_2
		if float(l2fc) < float('inf'):
			l2fc_max = max(l2fc_max,float(l2fc))
		if (flag == "yes") and (float(l2fc) > 0) and (sample_1 != sample_2):
			out_line = "\t".join([chrom,start,end,antibody,l2fc])
			open_out.write(out_line + "\n")
	open_file.close()
	open_out.close()
	subprocess.call(["sed","-i","s/inf/%s/g"%str(l2fc_max),out_file])
	sys.stderr.write(str(l2fc_max)+"\n")

if __name__ == '__main__':
	in_fn = sys.argv[1]
	ot_fn = sys.argv[2]
	main(in_fn,ot_fn)