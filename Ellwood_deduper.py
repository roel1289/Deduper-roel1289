#!/usr/bin/env python

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="A program to hold input + output file name")
    parser.add_argument("-f", "--file", help="designates absolute file path to sorted sam file", type = str)
    #parser.add_argument("-o", "--outfile", help="designates absolute file path to sorted sam file", type = str)
    parser.add_argument("-u", "--umi", help="designates file containing the list of UMIs", type = str)
    #parser.add_argument("-h", "--help", help="prints a USEFUL help message (see argparse docs)", type = str)
    return parser.parse_args()
    
args = get_args()

# ./<your_last_name>_deduper.py -u STL96.txt -f <in.sam> -o <out.sam>



# def umi_checker(qname):
#     '''placeholder... sample in/out'''
#     umi_line = re.findall('[ACTGUN]{0,8}',qname)
#     umi = umi_line[len(umi_line)-2]
#     return umi


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
        print(UMIs)
    return(UMIs)
    

umi_adder(args.umi)
# print(len(UMIs))

###########################################
#CIGAR string function

def startpositionCigarString(sam_file):
    '''This function will will take a sam file and extract start position and CIGAR string from a sam file header. The function will use the cigar string and return an adjusted start positon if there is soft clipping.'''
    with open(args.file, "r") as fh:
        CIGARstring = []
        StartPos = []
        
        #regex = re.search('(\d+)[S]')

        for line in fh:
            line = line.strip()
            if line.startswith("@"):
                continue
            else:
                CIGARstring = line.split('\t')[5]
                StartPos = line.split('\t')[3]

                result = re.findall(r'(\d+)[S]', CIGARstring)
                # determing if rev complement or not (rev comp = True)
                bflagList = line.split('\t')[1]
                flag = int(bflagList)

                #rev complement is true
                if((flag & 16) == 16):
                    for match in result:
                        StartPos = int(line.split('\t')[3]) - int(match)
                else:
                    for match in result:
                        StartPos = int(line.split('\t')[3]) + int(match)

                # for match in result:
                #     StartPos = int(line.split('\t')[3]) + int(match)
                #     #print(StartPos)
                    
            print(StartPos)
    return(StartPos)

startpositionCigarString(args.file)

# def bitwiseInterpreter(integer, bitwiseflag):
#    ```This function will input a bitwise integer and output True or false. Later on I will use this to determine if the read is + or - . ```



# UMI_dict = dict()

# unknownUMI_dict = dict()

#read in UMI file, and then save UMIs into dictionary

#close UMI file

#./Ellwood_deduper.py -f test1.sam -u STL96.txt