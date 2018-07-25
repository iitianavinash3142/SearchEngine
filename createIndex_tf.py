
#!/usr/bin/env python
import os.path, time, os
import sys
import re
from porterStemmer import PorterStemmer
from collections import defaultdict
from array import array
import gc
import math

porter=PorterStemmer()

class CreateIndex:

    def __init__(self):
        self.index=defaultdict(list)    #the inverted index
        self.tf=defaultdict(list)          #term frequencies of terms in documents
        self.df=defaultdict(int)         #document frequencies of terms in the corpus
        self.indx=defaultdict(list)    #the inverted index
        self.numDocuments=0

    
    def getStopwords(self):
        '''get stopwords from the stopwords file'''
        f=open(self.stopwordsFile, 'r')
        stopwords=[line.rstrip() for line in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()
        

    def getTerms(self, line):
        '''given a stream of text, get the terms from the text'''
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ',line) #put spaces instead of non-alphanumeric characters
        line=line.split()
        line=[x for x in line if x not in self.sw]  #eliminate the stopwords
        line=[ porter.stem(word, 0, len(word)-1) for word in line]
        return line

    def writeIndexToFile(self):
        

        f=open(self.timeIndex, 'w')
        print >>f, float(time.time())
        f.close()

        '''write the index to the file'''
        #write main inverted index

        f=open(self.indexFile, 'w')
        #first line is the number of documents
        print >>f, int(self.numDocuments)
        self.numDocuments=float(self.numDocuments)
        for term in self.index.iterkeys():
            postinglist=[]
            for p in self.index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            #print data
            postingData=';'.join(postinglist)
            tfData=','.join(map(str,self.tf[term]))
            idfData='%.4f' % (self.numDocuments/self.df[term])
            print >> f, '|'.join((term, postingData, tfData, idfData))
        f.close()

        f=open(self.indxFile, 'w')
        #first line is the number of documents
        print >>f, int(self.numDocuments)
        self.numDocuments=float(self.numDocuments)
        for term in self.indx.iterkeys():
            postinlist=[]
            for pq in self.indx[term]:
                docI=pq[0]
                positios=pq[1]
                postinlist.append(':'.join([str(docI) ,','.join(map(str,positios))]))
            #print data
            postinData=';'.join(postinlist)
            print >> f, '|'.join((term, postinData))
        f.close()

    def getParams(self):
        '''get the parameters stopwords file, collection file, and the output index file'''
        self.timeIndex='timeIndex.txt'        
        self.stopwordsFile='stopWords.txt'
        self.indexFile='testIndex.txt'
        self.indxFile='testtIndex.txt'        
        self.pnum=0
        self.fname='new'

    def createIndex(self):
        '''main of the program, creates the index'''
        self.getParams()
        for pdf_loop in range (1,len(sys.argv)):        	
            self.collFile = open(sys.argv[pdf_loop],'r')
            self.numDocuments+=1
            self.getStopwords()
            ame=sys.argv[pdf_loop]
            tr=ame.split("/")
            self.fname=tr[2]

            gc.disable()
            
            self.pnum=0
            x=0
            termdicPage={}
            termdictPage={}     
            for line in self.collFile:
        		
                #bug in python garbage collector!
        		#appending to list becomes O(N) instead of O(1) as the size grows if gc is enabled.
        		
        		#main loop creating the index                                
            	ters=self.getTerms(line)
            	self.pnum+=1

            	#build the index for the current page

            	for position, term in enumerate(ters,x):
            	    try:
            	        termdicPage[term][1].append(self.pnum)
                        termdictPage[term][1].append(position)

            	    except:
            	        termdicPage[term]=[self.fname, array('I',[self.pnum])]
                        termdictPage[term]=[self.fname, array('I',[position])]

                    x=position + 1    
            
            #merge the current page index with the main index
            for termPag, postinPage in termdicPage.iteritems():
               	self.indx[termPag].append(postinPage)
 	
            #normalize the document vector
            norm=0
            for term, posting in termdictPage.iteritems():
                norm+=len(posting[1])**2
            norm=math.sqrt(norm)
            
            #calculate the tf and df weights
            for term, posting in termdictPage.iteritems():
                self.tf[term].append('%.4f' % (len(posting[1])/norm))
                self.df[term]+=1
            
            #merge the current page index with the main index
            for termPage, postingPage in termdictPage.iteritems():
               	self.index[termPage].append(postingPage)  

            gc.enable()
            
            self.writeIndexToFile()
        
    
if __name__=="__main__":
    c=CreateIndex()
    c.createIndex()                   
    

