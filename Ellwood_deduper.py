#!/usr/bin/env python

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser(description="A program to hold input + output file name")
    parser.add_argument("-f", "--file", help="designates absolute file path to sorted sam file", type = str)
    parser.add_argument("-o", "--outfile", help="designates absolute file path to sorted sam file", type = str)
    parser.add_argument("-u", "--umi", help="designates file containing the list of UMIs", type = str)
    #parser.add_argument("-h", "--help", help="prints a USEFUL help message (see argparse docs)", type = str)
    return parser.parse_args()
    
args = get_args()

# ./<your_last_name>_deduper.py -u STL96.txt -f <in.sam> -o <out.sam>


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
    

#umi_adder(args.umi)
# print(len(UMIs))

###########################################
#CIGAR string function


# def softClip(line, cigar):
#     '''give in line and cigar string, then will output the adjusted start position'''
#     line = line.split()
#     pos = int(line[3])
#     bit_flag = int(line[1])

#     if reverse strand:

    # start position equals addition of all of the numbers















def startpositionCigarString(sam_file_line):
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

                #forward strand
                resultForward = re.findall(r'(\d+)[S]', CIGARstring)
                #reverse strand
                resultReverse = re.findall(r'(\d+)[S]', CIGARstring)
                #whole cigar string values:
                cigarSum = re.findall(r'[0-9]', CIGARstring)

                # determing if rev complement or not (rev comp = True)
                bflagList = line.split('\t')[1]
                flag = int(bflagList)

                #rev complement is true
                if((flag & 16) == 16):
                    for match in resultReverse: #start position plus readlen (100)
                        StartPos = int(line.split('\t')[3]) #plus rest of cigar string numbers
                else:
                    for match in resultForward:
                        StartPos = int(line.split('\t')[3]) + int(match)

                # for match in result:
                #     StartPos = int(line.split('\t')[3]) + int(match)
                #     #print(StartPos)
                    
            #print(StartPos)
    return(StartPos)

#startpositionCigarString(args.file)

#account for other things in cigar string (don't worry about H, = , P, or X)



#####################
def main(file):
    with open(args.file, "r") as inSam, open(args.outfile, "w") as outSam:
        
        #init dict. Key = startPos, value = [cigarstring, chrom, strand]
        #init dict. Key = (cigarstring, starpost, strand), value = chr
        main_dict = dict()
        membership_set = set()
        
        while True:
            line = inSam.readline().strip()
            if(line == ""):
                break
            if line.startswith("@"):
                continue
            else:
                parts = line.split('\t')
                StartPos = (parts[3]) #function to adjust start position
                chromosome = parts[2]
                strand = (parts[1]) #bitwise flag interpreter to see if it's stranded or not (TRUE or FALSE)
                UMI = parts[0].split(':')[-1]
                

                if (UMI, StartPos, chromosome, strand) not in membership_set:
                    membership_set.add(tuple((UMI, StartPos, chromosome, strand)))
                else:
                    continue


                print(membership_set)


        for key,values in main_dict.items():
            outSam.write(f'{main_dict[StartPos][0]}\t{main_dict[StartPos][1]}\t{StartPos}\t{main_dict[StartPos][2]}\n')



    return(outSam)

main(args.file)









#wipe dictionary memory every time we get to a new chromosome


# UMI_dict = dict()

# unknownUMI_dict = dict()

#read in UMI file, and then save UMIs into dictionary

#close UMI file

#./Ellwood_deduper.py -f test1.sam -u STL96 -o out_test.sam