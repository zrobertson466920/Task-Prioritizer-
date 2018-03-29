import numpy as np
import operator
from matplotlib import pyplot as mp

class Task():
    """Models tasks on a to-do list with priority and details fields"""

    def __init__(self,ctime,dtime,imp,desc):
        """Initialize task object"""
        self.ctime = ctime
        self.dtime = dtime

        self.time = 100 * ctime/dtime

        self.importance = imp
        self.priority = np.sqrt((ctime/dtime)*(ctime/dtime)+(imp)*(imp))
        self.desc = desc

def  print_sort(sorted_order):
    counter = 0
    for ita in sorted_order:
        counter += 1
        print(str(counter) + ": " + ita[0])

def print_csort(sorted_order,item):
    print("\n")
    counter = 0
    x = []
    y = []
    for ita in sorted_order:
        counter += 1
        print(str(counter) + ": " + ita[0])
        x.append(100 * item[ita[0]]['time'])
        y.append(item[ita[0]]['importance'])

    mp.scatter(x,y,s = 10)
    for i in range(counter):
        mp.annotate(str(i+1), (x[i],y[i]))

    mp.show()

def priority(item):
    return np.sqrt((100 * item['ctime']/item['dtime'])*(100 * item['ctime']/item['dtime'])+(item['importance'])*(item['importance']))
