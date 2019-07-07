
import task_directive as td
import output_directive as od
import operator
import json

import copy

import numpy as np
from operator import itemgetter

from matplotlib import pyplot as mp


def edit_task(tasks,index):
    field = 'd'
    e_task = tasks[index]
    while field != 'q':
        field = input("Enter field you'd like to edit: description (d), importance (i), due-time (t), est-time (e), start-time (s), quit (q) \n")
        if (field == 'd'):
            desc = input("Enter new description. \n")
            e_task.description = desc

        elif (field == 'i'):
            importance = float(input("Enter new importance. \n"))
            e_task.importance = importance

        elif (field == 't'):
            dtime = float(input("Enter new due-time. \n"))
            e_task.due_time = dtime

        elif (field == 'e'):
            ctime = float(input("Enter new est-time. \n"))
            e_task.complete_time = ctime

        elif (field == 's'):
            stime = float(input("Enter new start-time. \n"))
            e_task.start_time = stime

        elif (field == 'q'):
            return e_task


def task_loop(tasks,command):
    if command == 'a':
        desc = input("Write a short description of the task below. \n")
        importance = float(
            input("On a scale of (0 - 100) how important is the task? (Hint: Interpret as percentile)\n"))
        dtime = float(input("Input estimate of free time available to work on task. (Hours)\n"))
        ctime = float(input("Input estimate of time to complete the task. (Hours)\n"))
        stime = float(input("Input estimate of how long until task can be started. \n"))
        new_task = td.Task(ctime, dtime, importance, desc,start_time = stime)

        history.write('Making New Task ' + str(new_task.id) + "\n")
        json.dump(td.tasks_to_dict([new_task]), history)
        history.write('\n')

        tasks.append(new_task)
        tasks = td.sort_tasks(tasks)
        display_tasks(tasks)

    elif command == 'd':
        index = int(input("Input index of finished task. \n")) - 1

        history.write("Finished Task " + str(tasks[index].id) + "\n")

        del tasks[index]
        tasks = td.sort_tasks(tasks)
        display_tasks(tasks)

    elif command == 'e':
        index = int(input("Input index of task to edit. \n")) - 1
        display_task(tasks[index])
        edited_task = edit_task(tasks, index)

        history.write("Edited Task " + str(tasks[index].id) + "\n")
        json.dump(td.tasks_to_dict([tasks[index]]), history)
        history.write('\n')

        tasks = td.sort_tasks(tasks)
        display_tasks(tasks)

    elif command == 't':
        delta_time = float(input("Advance Time By How Much?\n"))
        for task in tasks:
            task.due_time += -delta_time
            task.start_time += -delta_time
            if task.start_time < 0:
                task.start_time = 0
        tasks = td.sort_tasks(tasks)
        history.write('Advanced Time ' + str(delta_time) + "\n")
        display_tasks(tasks)

    elif command == 'g':

        session_len = float(input("How long is a session? "))
        time_len = int(input("How many sessions? "))

        tasks = td.sort_tasks(td.load_tasks(current_tasks_path))
        # Make 100 random directives
        directives, actions = td.make_directives(tasks, session_len, time_len)

        # Evolve directives
        e_data = []
        for d, a in zip(directives, actions):
            e_data.append(td.evolve_directive(d, a, tasks, session_len, 500))

        # Pick best directive
        e_data.sort(key=itemgetter(2), reverse=True)
        display_directive(e_data[0][0][0:time_len])
        print("Projected Completion Rate: " + str(e_data[0][2]) + " out of " + str(len(tasks)) + "\n")

    elif command == 'q':
        td.save_tasks(tasks, current_tasks_path)
        task_matrix(tasks)
        work_distribution(tasks)
        history.close()

    return tasks


def task_matrix(tasks):
    print("\nPrinting Suggested Priority Ordering...")
    sorted_order = td.sort_tasks(tasks)
    counter = 0
    total_time = 0
    due_time = 0
    x = []
    y = []
    for item in sorted_order:
        if item.due_time <= 0:
            print("Time is expired for " + item.description)
            continue
        counter += 1
        print(str(counter) + ": " + item.description)
        total_time += item.complete_time
        due_time += item.due_time
        x.append(100 * item.complete_time / (item.due_time-item.start_time))
        y.append(item.importance)

    print()
    print("Usually items in the top right are Do-Now, top left are Schedule")
    print("bottom left are Delegate/Delay, and bottom right are Delete/Cut-Corners")
    print()
    print("Estimated time to finish task list is " + str(total_time) + " hrs.\n")

    ax = 0
    ay = 0
    mp.scatter(x, y, s=50)
    for i in range(counter):
        mp.annotate(str(i + 1), (x[i] + 0.12, y[i] - 0.12))
        ax += x[i] / counter
        ay += y[i] / counter

    mp.annotate("0", (ax, ay))

    mp.xlabel('Urgency (est-time / due-time)', fontsize=12)
    mp.ylabel('Importance (percentile)', fontsize=12)
    mp.title('Priority Matrix', fontsize = 13)
    mp.savefig('image.png',dpi = 600)
    mp.show()
    return


def work_distribution(tasks):
    print("Printing Distribution of Work Tasks")
    data = []
    for task in tasks:
        data.append((task.due_time,task.complete_time,task.start_time))
    data.sort(key=itemgetter(0))

    dist = np.repeat(0.0,int(data[-1][0]))
    for item in data:
        dist = dist + distribute(item,int(data[-1][0]))

    mp.plot(dist)
    mp.xlabel('Time Into the Future', fontsize = 12)
    mp.ylabel('Work Rate', fontsize = 12)
    mp.title("Work Distribution", fontsize = 13)
    mp.show()
    return


def distribute(item,stop):
    dist = []
    for i in range(0,stop):
        if item[2] <= i < item[0]:
            dist.append(float(item[1]) / float(item[0] - item[2]))
        else:
            dist.append(0)
    return np.array(dist)


def display_tasks(tasks):
    for i in range(len(tasks)):
        print(str(i+1) + ": " + tasks[i].description + " | due in " + str(tasks[i].due_time) + " hours.")
    print("\n")
    return


def display_task(task):
    print(task.description + " | importance " + str(task.importance) + " | due-time " + str(task.due_time) + " | est-time " + str(task.complete_time))
    print("\n")
    return


def display_directive(directive):

    for action in directive:
        print(action.description)
    return


if __name__ == '__main__':

    current_tasks_path = 'current_tasks.json'
    all_tasks_path = 'all_tasks.json'
    output_name = 'directive.txt'

    command = 'z'
    while command != 'q':
        command = input("Enter a command: View Tasks (v), Output Tasks to Document (o), Quit (q)\n")
        if command == 'v':

            print("Loading Current Tasks")
            current_tasks = td.sort_tasks(td.load_tasks(current_tasks_path))
            display_tasks(current_tasks)
            history = open(all_tasks_path, 'a')

            while command != 'q':
                command = input("Enter a command: Add Task (a), Delete Task (d), Edit Task (e), Advance Time (t), Generate Schedule (g), Save & Quit (q) \n")
                current_tasks = task_loop(current_tasks,command)
            command = 'v'

        elif command == 'o':
            od.basic_list(current_tasks_path)


