import task
import operator
from matplotlib import pyplot as mp

def main():

    item = []

    while (input("Would you like to add a task? (y/n) ") == 'y'):

        ctime = float(input("Input estimate of time to complete the task.\n"))
        dtime = float(input("Input estimate number of free hours available to work on task.\n"))
        importance = float(input("On a scale of (0 - 100) how important is the task?\n"))
        desc = input("Write a short description of the task below.\n")

        item.append(task.Task(ctime,dtime,importance,desc))

    sorted_item = sorted(item, key = operator.attrgetter('priority'))

    print("\n")
    counter = 0
    x = []
    y = []
    for ita in sorted_item[::-1]:
        counter += 1
        print(str(counter) + ": " + ita.desc)
        x.append(ita.time)
        y.append(ita.importance)

    mp.scatter(x,y,s = 10)
    for i in range(counter):
        mp.annotate(str(i+1), (x[i],y[i]))

    mp.show()


main()
