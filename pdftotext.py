import os
import sys
import glob
import string

# Create a directory for converted text files
text_directory = "Texts"				
if not os.path.exists(text_directory):
	os.makedirs(text_directory)

# Check if PDF directory exists
if os.path.isdir("PDFs") == False:
	print "There is no PDFs directory"

# For each file in the PDF directory run pdf2txt.py and direct stdout to txt file

for pdf in glob.glob("./PDFs/*.pdf"):
	filename = string.replace(pdf, "PDFs", "Texts")
	filename = string.replace(filename, ".pdf", ".txt")
	print "Converting ", pdf, "to plain text for analysis"
	os.system("python ./src/pdf2txt.py \"" + pdf + "\" >> \"" + filename+"\"")
	