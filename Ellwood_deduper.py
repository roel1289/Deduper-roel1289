#!/usr/bin/env python

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="A program to hold input + output file name")
    parser.add_argument("-f", "--file", help="designates absolute file path to sorted sam file", type = str)
    parser.add_argument("-o", "--outfile", help="designates absolute file output sam", type = str)
    #parser.add_argument("-o2", "--outDup", help="Output file of the duplicate PCR reads", type = str)
    parser.add_argument("-u", "--umi", help="designates file containing the list of UMIs", type = str)
    #parser.add_argument("-h", "--help", help="This programs takes a sorted sam file as input, and outputs a new sam file where all of the PCR duplicates have been removed. It also reports how many PCR duplicates were removed.", type = str)
    return parser.parse_args()
    
args = get_args()

# ./<your_last_name>_deduper.py -u STL96.txt -f <in.sam> -o <out.sam>

##########################################
# Functions
##########################################
# get list of the known UMIs
UMIs = []

def umi_adder(umi):
    '''This function creates a list of the UMIs based on a given file that contains all of the UMIs'''
    with open(args.umi, "r") as fh:
        while True:
            line = fh.readline().split()
            if(line == []):
                break
            #print(line)
            UMIs.append(line)
        #print(UMIs)
    return(UMIs)
    

umi_adder(args.umi)
# print(len(UMIs))
##########################################

############################################3
#determine if it's on the forward or reverse strand
def is_minus_strand(bit_flag):
    '''This function interprets bitwise flag. and return direction of the flag'''
    return (bit_flag & 0x10) != 0
############################################
#return new start position
def startpositionCigarString(line, cigar):
    '''This function will will take a sam file and extract start position and CIGAR string from a sam file header. The function will use the cigar string and return an adjusted start positon if there is soft clipping.'''
    line = line.split()
    position = int(line[3])
    adjusted_position = 0

    num_S = 0
    num_M = 0
    num_D = 0
    num_N = 0

    bit_flag = int(line[1])
    strand = is_minus_strand(bit_flag)

    cigar_parts = re.findall(r'(\d+)([MIDNSHPX=])', cigar)
        
    #neg strand
    if strand:
        for i,tup in enumerate(cigar_parts):
            if i == 0 and 'S' in tup:
                continue
            elif 'S' in tup:
                num_S += int(tup[0])
            elif 'M'in tup:
                num_M += int(tup[0])
            elif 'D' in tup: 
                num_D += int(tup[0])
            elif 'N' in tup:
                num_N += int(tup[0])
            
        adjusted_position = position + num_S + num_M + num_D + num_N 
            

    #pos strand
    else:
        if 'S' in cigar_parts[0]:
            adjusted_position = position - int(cigar_parts[0][0])
        else:
            adjusted_position = position


    return adjusted_position



###############################################
def main(file):
    duplicate = 0
    prev_chrom = None
    

    with open(args.file, "r") as inSam, open(args.outfile, "w") as outSam: # open(args.outDup, "w") as outDup:
        
        #init dict. Key = startPos, value = [cigarstring, chrom, strand]
        #init dict. Key = (cigarstring, starpost, strand), value = chr
        main_dict = dict()
        membership_set = set()
        
        
        while True:
            line = inSam.readline().strip()
            if(line == ""):
                break
            if line.startswith("@"):
                outSam.write(f'{line}\n')
            else:
                parts = line.split('\t')
                cigar = parts[5]
                StartPos = startpositionCigarString(line, cigar) #function to adjust start position
                chromosome = parts[2]

                bit_flag = int(parts[1])
                strand = is_minus_strand(bit_flag) #bitwise flag interpreter to see if it's stranded or not (TRUE or FALSE)
                UMI = parts[0].split(':')[-1]
                

                if (UMI, StartPos, chromosome, strand) not in membership_set:
                    membership_set.add(tuple((UMI, StartPos, chromosome, strand)))
                    outSam.write(f'{line}\n')
                else:
                    duplicate+=1
                    continue



        # for tup in membership_set:
        #     #print(f'{parts[0]}\t{parts[1]}\t{parts[2]}\t{tup[1]}\t{parts[4]}\t{parts[5]}\t{parts[6]}\t{parts[7]}\t{parts[8]}\t{parts[9]}\t{parts[10]}\n')
        #     outSam.write(f'{parts[0]}\t{parts[1]}\t{parts[2]}\t{tup[1]}\t{parts[4]}\t{parts[5]}\t{parts[6]}\t{parts[7]}\t{parts[8]}\t{parts[9]}\t{parts[10]}\n')


        # # if any(x not in membership_set for x):
        # #     print(membership_set)
        # filtered = [x for x in membership_set if (x) != chromosome]
        # print(filtered)

    #for tup in membership_set:
        if parts[2] != prev_chrom:     
            membership_set.clear()
            prev_chrom = chromosome
        
        #print(membership_set)
        print(duplicate)
               



    return(outSam)

main(args.file)


#for testing:
#./Ellwood_deduper.py -f test1.sam -u STL96.txt -o out_test.sam