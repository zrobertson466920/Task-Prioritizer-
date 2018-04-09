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

def print_sort(sorted_order,item):
    counter = 0
    for ita in sorted_order:
        counter += 1
        print(str(counter) + ": " + ita[0] + " | due in " + str(item[ita[0]]['dtime']) + " hours.")

def print_csort(sorted_order,item):
    print("\nPrinting Suggested Priority Ordering...")
    counter = 0
    x = []
    y = []
    for ita in sorted_order:
        counter += 1
        print(str(counter) + ": " + ita[0])
        x.append(100 * item[ita[0]]['ctime'] / item[ita[0]]['dtime'])
        y.append(item[ita[0]]['importance'])

    print("\n Usually items in the top right are Do-Now, top left are Schedule")
    print("bottom left are Delegate/Delay, and bottom right are Delete/Cut-Corners")

    ax = 0
    ay = 0
    mp.scatter(x,y,s = 10)
    for i in range(counter):
        mp.annotate(str(i+1), (x[i],y[i]))
        ax += x[i] / counter
        ay += y[i] / counter

    mp.annotate("0", (ax,ay))

    mp.xlabel('Urgency (est-time / due-time)', fontsize = 12)
    mp.ylabel('Importance (percentile)', fontsize = 12)

    mp.show()

def print_task(item):
    print("\nNeeds to be finished in " + str(item['dtime']) + " hours.")
    print("You plan to be finished in " + str(item['ctime']) + " hours.")
    print("The task has " + str(item['importance']) + "-th percentile importance.\n")

def priority(item,items):
    ux = 0
    uy = 0
    counter = 0
    for key,value in items.items():
        counter += 1
        ux += (100 * items[key]['ctime'] / items[key]['dtime'])
        uy += (items[key]['importance'])
    ux = ux / counter
    uy = uy / counter

    utime = 100 * item['ctime'] / item['dtime']
    uimp = item['importance']

    pr = 0
    if (ux - utime < 0):
        pr += 1
    if (uy - uimp < 0):
        pr += 1.5

    return pr
