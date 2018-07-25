
#!/usr/bin/env python
import os.path, time, os
import sys
from array import array
import gc
import math


class Time:           

    def getParams(self):        
        self.timeIndex='timeIndex.txt'
        self.fname='new'
        self.time=0

        f=open(self.timeIndex, 'r')
        time=[line.rstrip() for line in f]
        self.time=float(time[0])
        f.close()

    def timer(self):
        self.getParams()
        for loop in range (1,len(sys.argv)):
            part=sys.argv[loop]
            tr=part.split("/")
            self.fname=tr[2]
            file_mod_time = round(os.stat(sys.argv[loop]).st_mtime)
            file_cre_time = round(os.stat(sys.argv[loop]).st_ctime)

            if self.time-file_mod_time <= 0 or self.time-file_cre_time <= 0:
            	print self.fname
                    
    
if __name__=="__main__":
    c=Time()
    c.timer()                   
    

