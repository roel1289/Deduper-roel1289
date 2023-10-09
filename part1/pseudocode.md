Deduper Pseudocode:


Problem: 
When running PCR during the library prep stage of sequencing, it sometimes happens  
where an exact duplicate molecule is produced. The issue is if we leave these  
duplicates in our data, problems further downstream will arise such as thinking certain reads are  
expressed more than they actually are.  
The way to combat this is to take a SAM file containing uniquely mapped reads and a text file containing all known UMIs  
and remove PCR duplicates at this point. 

Examples:
An example SAM file is shown in this [folder](../STL96.txt). 

Pseudocode algorithm:
