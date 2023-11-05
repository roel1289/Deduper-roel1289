#!/usr/bin/env python

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="A program to hold input + output file name")
    parser.add_argument("-f", "--file", help="designates absolute file path to sorted sam file", type = str)
    parser.add_argument("-o", "--outfile", help="designates absolute file output sam", type = str)
    #parser.add_argument("-o2", "--outDup", help="Output file of the duplicate PCR reads", type = str)
    parser.add_argument("-u", "--umi", help="designates file containing the list of UMIs", type = str)
    #parser.add_argument("-h", "--help", help="prints a USEFUL help message (see argparse docs)", type = str)
    return parser.parse_args()
    
args = get_args()

# ./<your_last_name>_deduper.py -u STL96.txt -f <in.sam> -o <out.sam>

##########################################
# Functions
##########################################

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
def is_minus_strand(bit_flag):
    '''This functino interprets bitwise flag. and return direction of the flag'''
    return (bit_flag & 0x10) != 0
############################################

def startpositionCigarString(line, cigar):
    '''This function will will take a sam file and extract start position and CIGAR string from a sam file header. The function will use the cigar string and return an adjusted start positon if there is soft clipping.'''

    line = line.split()
    position = int(line[3])

    #initiating variables
    num_M = 0
    num_D = 0
    num_N = 0
    softClipRight = 0
    softClipLeft = 0

    bit_flag = int(line[1])
    strand = is_minus_strand(bit_flag)

    pattern = r'(\d+)S$'
    left_pattern = r'(\d+)S(?=\d+M)'

    match = re.search(pattern, cigar)
    left_match=re.findall(left_pattern, cigar)
    cigar_parts = re.findall(r'(\d+)([MIDNSHPX=])', cigar)

    for length, operation in cigar_parts:
        length = int(length)
        if operation == 'M':
            num_M += length
        elif operation =='D':
            num_D += length
        elif operation == 'N':
            num_N += length
        elif operation =='S' and strand and match:
            softClipRight = int(match.group(1))
        elif operation =='S' and not strand and left_match:
            softClipLeft = int(left_match[-1])
    if strand:
        adjusted_position = position + num_M + int(softClipRight) + num_D + num_N
    else:
        adjusted_position = position - softClipLeft
    return adjusted_position


#     CIGARstring = line.split('\t')[5]
#     StartPos = line.split('\t')[3]

#     #forward strand
#     resultForward = re.findall(r'(\d+)[S]', CIGARstring)
#     #reverse strand
#     resultReverse = re.findall(r'(\d+)[S]', CIGARstring)
#     #whole cigar string values:
#     cigarSum = re.findall(r'[0-9]', CIGARstring)

#     # determing if rev complement or not (rev comp = True)
#     bflagList = line.split('\t')[1]
#     flag = int(bflagList)

#     #rev complement is true
#     if((flag & 16) == 16):
#         for match in resultReverse: #start position plus readlen (100)
#             StartPos = int(line.split('\t')[3]) #plus rest of cigar string numbers
#     else:
#         for match in resultForward:
#             StartPos = int(line.split('\t')[3]) - int(match)

#             # for match in result:
#             #     StartPos = int(line.split('\t')[3]) + int(match)
#             #     #print(StartPos)
                    
#             #print(StartPos)
#     return(StartPos)

# #startpositionCigarString(args.file)

#account for other things in cigar string (don't worry about H, = , P, or X)


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









#wipe dictionary memory every time we get to a new chromosome


# UMI_dict = dict()

# unknownUMI_dict = dict()

#read in UMI file, and then save UMIs into dictionary

#close UMI file

#./Ellwood_deduper.py -f test1.sam -u STL96.txt -o out_test.sam