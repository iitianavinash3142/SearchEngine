#!/usr/bin/env python

import sys
import re
from porterStemmer import PorterStemmer
from collections import defaultdict
import copy

porter=PorterStemmer()

class QueryIndex:

    def __init__(self):
        self.index={}
        self.lineindex={}
        #self.titleIndex={}
        self.tf={}      #term frequencies
        self.idf={}    #inverse document frequencies


    def intersectLists(self,lists):
        if len(lists)==0:
            return []
        #start intersecting from the smaller list
        lists.sort(key=len)
        return list(reduce(lambda x,y: set(x)&set(y),lists))
        
    
    def getStopwords(self):
        f=open(self.stopwordsFile, 'r')
        stopwords=[line.rstrip() for line in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()
        

    def getTerms(self, line):
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ',line) #put spaces instead of non-alphanumeric characters
        line=line.split()
        line=[x for x in line if x not in self.sw]
        line=[ porter.stem(word, 0, len(word)-1) for word in line]
        return line
        
    
    def getPostings(self, terms):
        #all terms in the list are guaranteed to be in the index
        return [ self.index[term] for term in terms ]
    
    
    def getDocsFromPostings(self, postings):
        #no empty list in postings
        return [ [x[0] for x in p] for p in postings ]


    def readIndex(self):
        #read main index
        f=open(self.indexFile, 'r');
        #first read the number of documents
        self.numDocuments=int(f.readline().rstrip())
        for line in f:
            line=line.rstrip()
            term, postings, tf, idf = line.split('|')    #term='termID', postings='docID1:pos1,pos2;docID2:pos1,pos2'
            postings=postings.split(';')        #postings=['docId1:pos1,pos2','docID2:pos1,pos2']
            postings=[x.split(':') for x in postings] #postings=[['docId1', 'pos1,pos2'], ['docID2', 'pos1,pos2']]
            postings=[ [x[0], map(int, x[1].split(','))] for x in postings ]   #final postings list  
            self.index[term]=postings
            #read term frequencies
            tf=tf.split(',')
            self.tf[term]=map(float, tf)
            #read inverse document frequency
            self.idf[term]=float(idf)
        f.close()
       
        ##### Read line Index For Each Term #######         
 
        f=open(self.linefile, 'r');
        #first read the number of documents
        self.numDocuments=int(f.readline().rstrip())
        for line in f:
            line=line.rstrip()
            term, postings = line.split('|')    #term='termID', postings='docID1:pos1,pos2;docID2:pos1,pos2'
            postings=postings.split(';')        #postings=['docId1:pos1,pos2','docID2:pos1,pos2']
            postings=[x.split(':') for x in postings] #postings=[['docId1', 'pos1,pos2'], ['docID2', 'pos1,pos2']]
            postings=[ [x[0], map(str, x[1].split(','))] for x in postings ]   #final postings list  
            self.lineindex[term]=postings
        f.close()
        
        #read title index
        #f=open(self.titleIndexFile, 'r')
        #for line in f:
        #    pageid, title = line.rstrip().split(' ', 1)
        #    self.titleIndex[int(pageid)]=title
        #f.close()
        
     
    def dotProduct(self, vec1, vec2):
        if len(vec1)!=len(vec2):
            return 0
        return sum([ x*y for x,y in zip(vec1,vec2) ])
            
        
    def rankDocuments(self, terms, docs):
        #term at a time evaluation
        docVectors=defaultdict(lambda: [0]*len(terms))
        queryVector=[0]*len(terms)
        for termIndex, term in enumerate(terms):
            if term not in self.index:
                continue
            
            queryVector[termIndex]=self.idf[term]
            
            for docIndex, (doc, postings) in enumerate(self.index[term]):
                if doc in docs:
                    docVectors[doc][termIndex]=self.tf[term][docIndex]
                    
        #calculate the score of each doc
        docScores=[ [self.dotProduct(curDocVec, queryVector), doc] for doc, curDocVec in docVectors.iteritems() ]
        docScores.sort(reverse=True)
        resultDocs=[x[1] for x in docScores][:10]
       
        #### store lines for print #####
        
        if self.qt == "OWQ": 
           file_dic = {}   
        
            #for term in terms:
            #if term not in self.lineindex:
            #   continue  
            
           for x in self.lineindex[term]:
               if x[0] in resultDocs:
                  file_dic[x[0]] = x[1] 
                    
           #print document titles instead if document id's
           #resultDocs=[ self.titleIndex[x] for x in resultDocs ]
           #print '\n'.join(resultDocs), '\n'
        
           for k in resultDocs:
               lineno = ','.join(file_dic[k])
               result = k + " : " + lineno
               print result
           print '\n'

        if self.qt == "FTQ": 
           file_di = defaultdict(list)   
           file_dic = {}
           my_set = set()
           new_list = []
           for term in terms:
               if term not in self.lineindex:
                  continue  
            
               for x in self.lineindex[term]:
                   if x[0] in resultDocs:
                      file_di[x[0]].append(x[1]) 
           

           for txtfile in file_di:
               my_set.clear() 
               for li in file_di[txtfile]:
                   my_set = my_set.union(set(li))
                   new_list = list(my_set)

               file_dic[txtfile] = new_list           
           #print document titles instead if document id's
           #resultDocs=[ self.titleIndex[x] for x in resultDocs ]
           #print '\n'.join(resultDocs), '\n'
        
           for k in resultDocs:
               lineno = ','.join(file_dic[k])
               result = k + " : " + lineno
               print result
           print '\n'

        if self.qt == "PQ": 
           file_di = defaultdict(list)   
           file_dic = {}
           my_set = set()
           new_list = []
           for term in terms:
               if term not in self.lineindex:
                  continue  
            
               for x in self.lineindex[term]:
                   if x[0] in resultDocs:
                      file_di[x[0]].append(x[1]) 
           

           for txtfile in file_di:
               new_list = self.intersectLists(file_di[txtfile]) 
               
               file_dic[txtfile] = new_list           
           #print document titles instead if document id's
           #resultDocs=[ self.titleIndex[x] for x in resultDocs ]
           #print '\n'.join(resultDocs), '\n'
        
           for k in resultDocs:
               lineno = ','.join(file_dic[k])
               result = k + " : " + lineno
               print result
           print '\n'   


    def queryType(self,q):
        if '"' in q:
            return 'PQ'
        elif len(q.split()) > 1:
            return 'FTQ'
        else:
            return 'OWQ'


    def owq(self,q):
        '''One Word Query'''
        originalQuery=q
        q=self.getTerms(q)
        if len(q)==0:
            print 'Enter Correct Word'
            return
        elif len(q)>1:
            self.ftq(originalQuery)
            return
        
        #q contains only 1 term 
        term=q[0]
        if term not in self.index:
            print 'Not Found'
            return
        else:
            postings=self.index[term]
            docs=[x[0] for x in postings]
            self.rankDocuments(q, docs)
          

    def ftq(self,q):
        """Free Text Query"""
        q=self.getTerms(q)
        if len(q)==0:
            print 'Enter Correct Word'
            return
        
        li=set()
        for term in q:
            try:
                postings=self.index[term]
                docs=[x[0] for x in postings]
                li=li|set(docs)
            except:
                #term not in index
                pass
        
        li=list(li)
        self.rankDocuments(q, li)


    def pq(self,q):
        '''Phrase Query'''
        originalQuery=q
        q=self.getTerms(q)
        if len(q)==0:
            print 'Enter Correct Word'
            return
        elif len(q)==1:
            self.owq(originalQuery)
            return

        phraseDocs=self.pqDocs(q)
        self.rankDocuments(q, phraseDocs)
        
        
    def pqDocs(self, q):
        """ here q is not the query, it is the list of terms """
        phraseDocs=[]
        length=len(q)
        #first find matching docs
        for term in q:
            if term not in self.index:
                #if a term doesn't appear in the index
                #there can't be any document maching it
                return []
        
        postings=self.getPostings(q)    #all the terms in q are in the index
        docs=self.getDocsFromPostings(postings)
        #docs are the documents that contain every term in the query
        docs=self.intersectLists(docs)
        #postings are the postings list of the terms in the documents docs only
        for i in xrange(len(postings)):
            postings[i]=[x for x in postings[i] if x[0] in docs]
        
        #check whether the term ordering in the docs is like in the phrase query
        
        #subtract i from the ith terms location in the docs
        postings=copy.deepcopy(postings)    #this is important since we are going to modify the postings list
        
        for i in xrange(len(postings)):
            for j in xrange(len(postings[i])):
                postings[i][j][1]=[x-i for x in postings[i][j][1]]
        
        #intersect the locations
        result=[]
        for i in xrange(len(postings[0])):
            li=self.intersectLists( [x[i][1] for x in postings] )
            if li==[]:
                continue
            else:
                result.append(postings[0][i][0])    #append the docid to the result
        
        return result

        
    def getParams(self):
        #param=sys.argv
        self.stopwordsFile="stopWords.txt"
        self.indexFile="testIndex.txt"
        self.linefile="testtIndex.txt"
        #self.titleIndexFile=param[3]


    def queryIndex(self):
        self.getParams()
        self.readIndex()  
        self.getStopwords() 
        print "\n\n\nenter input search string or to exit searching press 'e'" 
        q=sys.stdin.readline()
        print "\n"
        while q[0] != 'e' :
            if q == 'e':
                break

            self.qt=self.queryType(q)
            if self.qt=='OWQ':
                self.owq(q)
            elif self.qt=='FTQ':
                self.ftq(q)
            elif self.qt=='PQ':
                self.pq(q)
            print "\n\n\nenter input search string or to exit searching press 'e'" 
            q=sys.stdin.readline()
        
if __name__=='__main__':
    q=QueryIndex()
    q.queryIndex()
