#!/bin/bash
#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=interactive               #REQUIRED: which partition to use
#SBATCH --mail-type=ALL                   #optional: must set email first, what type of email you want
#SBATCH --cpus-per-task=8                 #optional: number of cpus, default is 1
#SBATCH --mem=32GB                        #optional: amount of memory, default is 4GB

#go to deduper directory
# dir="/projects/bgmp/roel/bioinfo/Bi624/Deduper-roel1289"
# cd $dir

# #sort the sam files
# samtools sort -O sam -o C1_SE_uniqAlign.sorted.sam C1_SE_uniqAlign.sam

#run deduper script on the sorted sam file
/usr/bin/time -v ./Ellwood_deduper.py -f C1_SE_uniqAlign.sorted.sam -u STL96.txt -o out.sam 
