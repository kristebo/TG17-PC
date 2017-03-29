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

# text
+ HTML without:
  - \<html\>
  - \<head\>
  - \<body\>
  - \<script\>-tags.
+ bootstrap3 formatting-classes

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

# delivery will be on a own page.
  deliveri of one file username and task must be set.
  
# if needed  
Delivery through Dropbox -> use the username from geekevents. (private browser if needed)

