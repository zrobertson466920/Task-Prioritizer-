
import task
import operator
import json

def main():

    print("Loading Tasks...")
    file_path = 'tasks.json'
    try:
        f = open(file_path)
    except IOError:
        # If not exists, create the file
        f = open(file_path, 'w+')
        f.write("{}")
    with open("tasks.json", 'r') as f:
        item = json.load(f)

    order = {}

    for key, value in item.items():
        item[key]['priority'] = task.priority(value,item)
        order[key] = value['priority']

    sorted_order = sorted(order.items(), key = operator.itemgetter(1), reverse = True)
    task.print_sort(sorted_order,item)
    print("\n")

    command = 'a'
    while (command != 'q'):
        command = input("Enter a command: Add Task (a), Delete Task (d), Edit Task (e), Advance Time (t), Save & Quit (q) \n")

        if (command == 'a'):

            desc = input("Write a short description of the task below. \n")
            importance = float(input("On a scale of (0 - 100) how important is the task? (Hint: Interpret as percentile)\n"))
            dtime = float(input("Input estimate of free time available to work on task. (Hours)\n"))
            ctime = float(input("Input estimate of time to complete the task. (Hours)\n"))
            item[desc] = {'ctime' : ctime, 'dtime' : dtime, 'importance' : importance, 'time' : ctime/dtime, 'priority' : 0}
            item[desc]['priority'] = task.priority(item[desc],item)
            order[desc] = item[desc]['priority']
            sorted_order = sorted(order.items(), key = operator.itemgetter(1), reverse = True)
            task.print_sort(sorted_order,item)

        elif (command == 'd'):

            index = int(input("Input index of finished task. \n")) - 1
            del item[sorted_order[index][0]]
            del order[sorted_order[index][0]]
            del sorted_order[index]
            sorted_order = sorted(order.items(), key = operator.itemgetter(1), reverse = True)
            task.print_sort(sorted_order,item)

        elif (command == 'e'):

            index = int(input("Input index of task to edit. \n")) - 1
            field = 'd'
            task.print_task(item[sorted_order[index][0]])
            while (field != 'q'):

                field = input("Enter field you'd like to edit: description (d), importance (i), due-time (t), est-time (e), quit (q) \n")

                if (field == 'd'):
                    desc = input("Enter new description. \n")
                    item[desc] = item[sorted_order[index][0]]
                    order[desc] = item[desc]['priority']
                    del item[sorted_order[index][0]]
                    del order[sorted_order[index][0]]
                    sorted_order = sorted(order.items(), key = operator.itemgetter(1), reverse = True)
                    task.print_sort(sorted_order,item)
                elif (field == 'i'):
                    importance = input("Enter new importance. \n")
                    item[sorted_order[index][0]]['importance'] = float(importance)
                    order[sorted_order[index][0]] = task.priority(item[sorted_order[index][0]],item)
                    sorted_order = sorted(order.items(), key = operator.itemgetter(1), reverse = True)
                    task.print_sort(sorted_order,item)
                elif (field == 't'):
                    dtime = input("Enter new due-time. \n")
                    item[sorted_order[index][0]]['dtime'] = float(dtime)
                    order[sorted_order[index][0]] = task.priority(item[sorted_order[index][0]],item)
                    sorted_order = sorted(order.items(), key = operator.itemgetter(1), reverse = True)
                    task.print_sort(sorted_order,item)
                elif (field == 'e'):
                    dtime = input("Enter new est-time. \n")
                    item[sorted_order[index][0]]['ctime'] = float(dtime)
                    order[sorted_order[index][0]] = task.priority(item[sorted_order[index][0]],item)
                    sorted_order = sorted(order.items(), key = operator.itemgetter(1), reverse = True)
                    task.print_sort(sorted_order,item)

        elif (command == 't'):
            temp = input("Advance time by how much? \n")
            for key, value in item.items():
                item[key]['dtime'] = value['dtime'] - float(temp)
                item[key]['priority'] = task.priority(item[key],item)
                order[key] = value['dtime']
            sorted_order = sorted(order.items(), key = operator.itemgetter(1), reverse = True)
            task.print_sort(sorted_order,item)

        elif (command == 'q'):
            sorted_order = sorted(order.items(), key = operator.itemgetter(1), reverse = True)
            task.print_csort(sorted_order,item)
            with open("tasks.json", 'w') as f:
                json.dump(item,f)

main()
