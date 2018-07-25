import sys
from array import array
import gc
import math
import glob,os

temp_keyword = ""
for pdf_loop in range (1,len(sys.argv)):
	enter_keyword = sys.argv[pdf_loop]
	temp_keyword = temp_keyword + enter_keyword + " "
keyword = temp_keyword.split()
 
def computeLPSArray(keyword, M, lps):
    len = 0 # length of the previous longest prefix suffix
 
    lps[0] # lps[0] is always 0
    i = 1
 
    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if keyword[i]==keyword[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            if len != 0:
                len = lps[len-1]
 
            else:
                lps[i] = 0
                i += 1

def KMPSearch(keyword):
    f=open('timeIndex.txt', 'r')
    time=[line.rstrip() for line in f]
    timer=float(time[0])
    f.close()

    out = open('output.txt', 'w')
    #Search through every inputted pdf
    files = []
    for file in glob.glob("./Texts/*.txt"):
        if file == 'stopwords.txt':
            continue
        files.append(file)
	
    for file in files:
        file_cre_time = round(os.stat(file).st_ctime)

        if timer-file_cre_time <= 0:
            ar=file

            f = open(ar, 'r')
            text = f.read().lower().split()

            M = len(keyword)
            N = len(text)
            counter = 0
            where_appear = []
            appear = False
    
 
    # create lps[] that will hold the longest prefix suffix 
    # values for keywordtern
            lps = [0]*M
            j = 0 # index for keyword[]
 
    # Preprocess the keywordtern (calculate lps[] array)
            computeLPSArray(keyword, M, lps)
 
            i = 0 # index for text[]
            while i < N:
                if keyword[j] == text[i]:
                    i += 1
                    j += 1
 
                if j == M:
                    counter = counter + 1
                    where_appear.append(i-j)
                    appear = True
                #print "Found pattern at index " + str(i-j)
                    j = lps[j-1]
 
        # mismatch after j matches
                elif i < N and keyword[j] != text[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
                    if j != 0:
                        j = lps[j-1]
                    else:
                        i += 1   

            keyword_loop = j   

            tr=ar.split("/")
            fname=tr[2]
            if counter>0:
            	print  fname + " : " + str(counter) + " times"
            
KMPSearch(keyword)


