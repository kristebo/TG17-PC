# Build and run.
Run build.sh setting up deps and docker, and run.sh for setting up the flask app.

# tasks

tasks is a CSV-file with the following format:

_\_id,title,points,taskcontentpath_

# id
Integer

# title
title of the task

# taskcontentpath
en fil med beskrivelsen av oppgaven

# task content returned as json-objects:


# JSON
endpoints return these as json:
- __gettask__ - 
  the task description as described in text
- __tasks__ - 
  a list of the tasks
- __usertotalpoints__ - 
  the paricipants total points
- __taskstate__ - 
  a list of the participants that has done that task

# endpoinst
## delivery 
post request /tgpc/api/deliver
content: 
partname \<str\>
partid \<int\>
solution \<str\>

## all the other:
- /
returns "glalalla"
- /tgpc/api/gettask/\<int:taskid\>/\n
returns taskids content as json.
- /tgpc/api/tasks/\n
All the tasks as tasks: taskid, name and path
- /tgpc/api/taskstate/\<int:tasknr\>/\n
state of tasknr
- /tgpc/api/parttotal/\<partid\>\n
returns partname and sum
- /tgpc/api/leaderboard\n
yeah!
- /tgpc/api/ord \n
10k lines lines of words



  

