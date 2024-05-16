#!/bin/bash
#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --job-name=ThreadTest ### Job Name
#SBATCH --partition=bgmp               #REQUIRED: which partition to use
#SBATCH --time=2-00:00:00 ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --cpus-per-task=8                 #optional: number of cpus, default is 1
#SBATCH --mem=16GB                        #optional: amount of memory, default is 4GB

echo "1 thread"
/usr/bin/time -v samtools view -bS C1_SE_uniqAlign.sorted.sam > C1_SE_uniqAlign_1.sorted.bam

echo "8 threads"
/usr/bin/time -v samtools view -bS -@ 8 C1_SE_uniqAlign.sorted.sam > C1_SE_uniqAlign_8.sorted.bam
