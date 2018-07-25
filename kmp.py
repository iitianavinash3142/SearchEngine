import sys

temp_keyword = ""

enter_keyword = raw_input("Enter your keywords: ")
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
    out = open('output.txt', 'w')
    #Search through every inputted pdf
	
    for pdf_loop in range (1,len(sys.argv)):
        f = open(sys.argv[pdf_loop], 'r')
        text = f.read().lower().split()
	
        if len(text) < 100:
            out.write("ERROR: \nFile \"" + sys.argv[pdf_loop] + "\" is either suspiciously brief or cannot be read! \nPlease also check this one manually.\n")

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
  
        out.write("Keyword " + keyword[keyword_loop].upper() + " found in file: " + sys.argv[pdf_loop] + " " + str(counter) + " times \n \n")
        if appear == True:
            for i in range(0,len(where_appear)):
                try:
                    if where_appear[i] < 16:
                        out.write("\"",)
                        for j in range (0,30):
                            out.write(text[j] + " ",)
                        out.write("\"",)
                    elif where_appear[i] > len(text)-15:
                        out.write("\"",)
                        for j in range (len(text) - 30, len(text)):
                            out.write(text[j] + " ",)
                        out.write("\"",)
                    else:
                        out.write("\"",)
                        for j in range (-15,15):
                            if text[where_appear[i] + j] == keyword[keyword_loop]:
                                out.write(keyword[keyword_loop].upper() + " ")
                            else:
                                out.write(text[where_appear[i] + j] + " ",)
                        out.write("\"",)
                    out.write("\n")
                except IndexError:
                    for j in range (0,len(text)):
                        if text[where_appear[i] + j] == keyword[keyword_loop]:
                            out.write(keyword[keyword_loop].upper() + " ")
                        else:
                            out.write(text[where_appear[j]] + " ",)
                    out.write("\"",)
                out.write("\n")
                appear = False            
KMPSearch(keyword)

