import numpy as np
from operator import itemgetter
from matplotlib import pyplot as mp
import task_directive as td
import copy
import operator
from random import randint
import time
import json

import networkx as nx


class Task():
    """Models tasks on a to-do list with priority and details fields"""

    def __init__(self,complete_time,due_time,importance,description,time_id=-1,start_time = 0):
        """Initialize task object"""
        if time_id == -1:
            self.id = int(time.time())
        else:
            self.id = time_id

        self.complete_time = complete_time
        self.due_time = due_time
        self.start_time = start_time

        self.urgency = 100 * complete_time / (due_time-start_time)

        self.importance = importance
        self.priority = 0
        self.update_priority()
        self.description = description
        self.history = []
        self.update_history(self.id)
        return

    def update_priority(self):
        self.priority = np.sqrt((self.urgency+3*self.importance)**2)

    def update_history(self,timestamp):
        self.history.append((self.complete_time,self.due_time,self.urgency,self.importance,self.start_time,self.priority,self.description,timestamp))
        return


def load_tasks(file_path):
    try:
        f = open(file_path)
    except IOError:
        # If not exists, create the file
        f = open(file_path, 'w+')
        f.write("{}")
    with open(file_path, 'r') as f:
        item = json.load(f)
        tasks = []
        for key,value in item.items():
            tasks.append(Task(value[0],value[1],value[2],value[4],key,start_time = value[3]))
    f.close()
    return tasks


def tasks_to_dict(tasks):
    item = {}
    for task in tasks:
        item[str(task.id)] = [task.complete_time,task.due_time,task.importance,task.start_time,task.description,task.urgency,task.priority]
    return item


def save_tasks(tasks,file_path):
    with open(file_path, 'w') as f:
        item = tasks_to_dict(tasks)
        json.dump(item, f)
    f.close()
    return


def sort_tasks(tasks):
    """
    Sorts tasks by priority (descending)
    Args:
        tasks: List of task objects

    Returns:
        list: sorted tasks in list form
    """
    if len(tasks) == 0:
        return tasks

    criteria = []
    for task in tasks:
        task.update_priority()
        criteria.append(task.priority)

    task_tuple = list(zip(criteria,tasks))
    task_tuple.sort(key=itemgetter(0),reverse = True)
    _,sorted_tasks = zip(*task_tuple)

    return list(sorted_tasks)


def fitness(actions,tasks):
    """
    Calculates fitness for sequence of directive (only accepts action list at end) by computing completion rate

    Args:
        actions: list of tasks for each work session
        tasks: list of tasks

    Returns:
        fitness: completion rate of directive
        tasks_left: number of tasks left uncompleted by directive
    """

    fitness = 0
    for i in range(0,len(tasks)):
        fitness += (tasks[i].complete_time - actions[i].complete_time) / tasks[i].complete_time

    return fitness,len(tasks) - fitness


def rand_action(actions):
    """
    Selects a random action from list such that it cna be started
    and due-time/complete-time are positive.
    Args:
        actions: List of possible actions

    Returns:
        action: selected action

    """

    allowed = []
    for i in range(0,len(actions)):
        if actions[i].due_time > 0 and actions[i].complete_time > 0 and actions[i].start_time <= 0:
            allowed.append(i)
    allowed.append(len(actions)-1)
    index = randint(0,len(allowed)-1)
    return allowed[index]


def action_step(actions,step,index):
    """
    Steps available actions by selected action.
    All tasks in list have due-time/start-time changed
    and selected task has complete-time additionally adjusted.
    Args:
        actions: list of available actions
        step: time step size
        index: index of selected action for period

    Returns:
        actions: updated list of actions
    """

    for action in actions:
        action.due_time -= step
        action.start_time -= step
        if action.start_time < 0:
            action.start_time = 0

    actions[index].complete_time -= step
    if actions[index].complete_time < 0:
        actions[index].complete_time = 0

    return actions


def empty_task():
    """
    Allows for nothing to be done during a time-period
    Returns:
        empty_task: Empty Task

    """
    return Task(0,1,0,"Nothing")


def make_directives(tasks,step,num):
    """
    Make number of random directives
    Args:
        tasks: task list
        step: session length
        num: number of possible directive

    Returns:
        directives: possible policies
        actions: available tasks at end of policy

    """

    directives = []
    actions = []

    for i in range(0,num):
        a,b = rand_directive(tasks,step)
        directives.append(a)
        actions.append(b)

    return directives,actions


def evolve_directive(o_directive,o_actions,tasks,step,num):
    """
    Anneal directives for some number of steps
    Args:
        o_directive: original directive
        o_actions: original action list
        tasks: original task list
        step: session length
        num: how long to run annealing

    Returns:
        directive: annealed directive
        actions: annealed actions
        fitness: fitness of annealed directive

    """

    directive = copy.deepcopy(o_directive)
    actions = copy.deepcopy(o_actions)

    fitness = td.fitness(actions,tasks)[0]
    m_fitness = 0
    for i in range(0, num):
        m_c_directive, m_c_actions = td.m_c_directive(directive, tasks, step)
        m_fitness = td.fitness(m_c_actions, tasks)[0]
        if m_fitness >= fitness:
            fitness = m_fitness
            directive = copy.deepcopy(m_c_directive)
            actions = copy.deepcopy(m_c_actions)

    return directive,actions,fitness


def rand_directive(tasks,step):
    """
    Make a policy using random selection
    Args:
        tasks: task list
        step: session length

    Returns:
        directive: policy on task list
        actions: available actions at end

    """

    directive = []
    actions = copy.deepcopy(tasks)
    actions.append(empty_task())

    max_time = 0
    for task in tasks:
        if task.due_time >= max_time:
            max_time = task.due_time

    max_time = int(np.ceil(max_time / step))
    for t in range(0,max_time):
        index = rand_action(actions)
        directive.append(actions[index])
        actions = action_step(actions,step,index)

    return directive,actions


def find_action(actions,action):
    """
    Checks if action is available from action list
    Args:
        actions: list of available actions
        action: candidate action

    Returns:
        index: returns index if available otherwise -1

    """

    for i in range(0,len(actions)):
        if actions[i].description == action.description:
            return i
    return -1


def m_c_directive(directive,tasks,step):
    """
    Alters directive from random time point
    Args:
        directive: current directive
        tasks: task list
        step: session length

    Returns:
        m_c_directive: Changes random session action of
        original directive and keeps as closely to original policy
        after that.
        actions: available actions after change

    """

    m_c_directive = []
    actions = copy.deepcopy(tasks)
    actions.append(empty_task())

    max_time = 0
    for task in tasks:
        if task.due_time >= max_time:
            max_time = task.due_time
    max_time = int(np.ceil(max_time / step))
    time_r = randint(0,max_time-1)

    for t in range(0,max_time):
        if t < time_r:
            index = find_action(actions,directive[t])
            action = directive[t]
            m_c_directive.append(action)
            actions = action_step(actions, step, index)
        elif t == time_r:
            index = rand_action(actions)
            m_c_directive.append(actions[index])
            actions = action_step(actions, step, index)
        else:
            if find_action(actions,directive[t]) != -1:
                index = find_action(actions,directive[t])
                action = directive[t]
                m_c_directive.append(action)
                actions = action_step(actions, step, index)
            else:
                index = rand_action(actions)
                m_c_directive.append(actions[index])
                actions = action_step(actions, step, index)

    return m_c_directive,actions
