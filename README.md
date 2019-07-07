# Task-Directive
Uses a heuristic to order tasks in a to-do list and outputs a simple graph.

# Basic Usage

Once you start up the program you'll get three options. You can either view your current tasks, output your tasks to pdf document, or quit. On the first run, it'll automatically create a file for storing tasks. When you load tasks They'll be displayed in order of their priority. A description of the task will be available and the amount of time remaining to complete the task will also be displayed.

To add a task follow the prompt and type in 'a'. You'll need to fill in data for the various prompts. After you're done a display will be shown. An example is given below.

```
Enter a command: Add Task (a), Delete Task (d), Edit Task (e), Advance Time (t), Generate Schedule (g), Save & Quit (q) 
a
Write a short description of the task below. 
Finish README
On a scale of (0 - 100) how important is the task? (Hint: Interpret as percentile)
60
Input estimate of free time available to work on task. (Hours)
3.0
Input estimate of time to complete the task. (Hours)
0.75
Input estimate of how long until task can be started. 
0
1: Finish README | due in 5.0 hours.
2: Finish Topology | due in 35.0 hours
```

Pay attention to the second task. In my personal life, I each day has *five* working hours. Thus, if I have 35 hours to finish a task, that really means I have 7 days to finish it. I find reasoning in terms of smaller blocks to be a more accurate way to represent the true amount of time available for me to work on a task.

Once you're done entering tasks you can either quit, advance time, or generate a schedule. Quiting will bring you back to the original prompt. Advancing time will let you change the amount of available time for all of you're current tasks by a user inputed amount. Finally, generating a schedule will prompt the program to make a workflow for the current task list. An example is given below.

```
Enter a command: Add Task (a), Delete Task (d), Edit Task (e), Advance Time (t), Generate Schedule (g), Save & Quit (q) 
g
How long is a session? 0.5
How many sessions? 3
Finish README
Implement Forward Model
Implement Forward Model
Projected Completion Rate: 3.0 out of 3
```
I work best in thirty minute sessions. I currently have an hour an a half to work. At the very bottom a projection is dispalyed for how many of my tasks I'll be able to finish assuming I keep to the schedule it generates. The horizon for the prediction is *infinity*. This is useful for when you fall behind schedule and want to know whether or not it's okay to be done with work for the day. I'll commonly advance time by one day (5 hours) and then see whether or not the projection goes below 100%.

There a couple more experimental features. Once you quit, a graph will be displayed. It's based on the Eisenhower Matrix for task priority. It's also possible to display your current tasks in a PDF with an attached graphic. It is not *currently* possible to attach a generated schedule. Instead, tasks are ordered by priority. 

In the future I'm hoping to add hierarchy to the task creation so that way schedules can be generated for specific clusters of to-do items. Better integration with the PDF feature would also be nice. In the long term the ideal is a kind of web-app or reminder system to help accountability. 
