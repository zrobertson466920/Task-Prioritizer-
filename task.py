import numpy as np

class Task():
    """Models tasks on a to-do list with priority and details fields"""

    def __init__(self,ctime,dtime,imp,desc):
        """Initialize task object"""
        self.ctime = ctime
        self.dtime = dtime

        self.time = 100 * ctime/dtime

        self.importance = imp
        self.priority = np.sqrt((100) * (ctime/dtime)**(ctime/dtime)+(imp)**(imp))
        self.desc = desc

def priority(ctime,dtime,imp):
    return np.sqrt((100 * ctime/dtime)**(ctime/dtime)+(imp)**(imp))
