# todoist-reminder

`todoist_daemon.py -a API_KEY [-d for debug]`

Adds the ability to define reminders in the task description.

--------

![Call Mom on the 9th at noon !1d !1h !30m !10](https://i.imgur.com/tAWkmTh.png)

This example will add a reminder **1 day**, **1 hour**, **30 minutes** and **10 minutes** before the due date.

![](https://i.imgur.com/mI1eUPi.png)

After a few seconds, all that is left will be `Call Mom`.

![](https://i.imgur.com/YhdLFE9.png)

## Install

`todoist-reminder` runs continuously, so having it on a server or Raspberry Pi would be ideal.

It is only tested on Linux. 

You need:

- Python
- [The Python Todoist API](https://developer.todoist.com/#client-libraries)
