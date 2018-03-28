import task
import json
import operator
from matplotlib import pyplot as mp

def main():

    print("Loading Tasks...")
    with open("tasks.json", 'r') as f:
        item = json.load(f)

    order = {}

    for key, value in item.items():
        order[key] = value['priority']

    while (input("Would you like to add a task? (y/n) ") == 'y'):

        ctime = float(input("Input estimate of time to complete the task.\n"))
        dtime = float(input("Input estimate of time available to work on task.\n"))
        importance = float(input("On a scale of (0 - 100) how important is the task? (Hint: Interpret as percentile)\n"))
        desc = input("Write a short description of the task below.\n")

        item[desc] = {'ctime' : ctime, 'dtime' : dtime, 'importance' : importance, 'time' : ctime/dtime, 'priority' : task.priority(ctime,dtime,importance)}
        order[desc] = item[desc]['priority']

    sorted_item = sorted(order.items(), key = operator.itemgetter(1))

    print("Saving Tasks")
    with open("tasks.json", 'w') as f:
        json.dump(item,f)

    print("\n")
    counter = 0
    x = []
    y = []
    for ita in sorted_item[::-1]:
        counter += 1
        print(str(counter) + ": " + ita[0])
        x.append(item[ita[0]]['time'])
        y.append(item[ita[0]]['importance'])

    mp.scatter(x,y,s = 10)
    for i in range(counter):
        mp.annotate(str(i+1), (x[i],y[i]))

    mp.show()

main()
