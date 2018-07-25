#!/usr/bin/python
import os
import sys
import glob
import string

# Create a directory for converted text files
text_directory = "Texts"				
if not os.path.exists(text_directory):
	os.makedirs(text_directory)

argv = ""
arg_list = glob.glob("./Texts/*.txt")
for arg in arg_list:
	argv += "\""+arg+"\" "

print "1)to create index and search in folder\n2)to search in folder\n3)to convert pdf to text\n4)search in file by kmp\n5)recently modified or created files\n6)exit program\n"
q=int(input())	

while q != 6:
	if q==1:
    	 os.system("python ./createIndex_tf.py "+argv) 
    	 os.system("python ./queryIndex_tfidf.py ") 
	if q==2:
    	 os.system("python ./queryIndex_tf.py ")
	if q==3:
    	 os.system("python ./pdftotext.py ")
	if q==4:
		 ar=sys.stdin.readline()
		 os.system("python ./kmp.py "+ar)
	if q==5:
    	 os.system("python ./time.py "+argv) 
	
	print "\n1)to create index and search in folder\n2)to search in folder\n3)to convert pdf to text\n4)search in file by kmp\n5)recently modified or created files\n6)exit program\n"

	q=int(input()) 

    