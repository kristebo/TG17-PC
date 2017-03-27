#Build and run.
Run build.sh setting up deps and docker, and run.sh for setting up the flask app.

#tasks

tasks is a CSV-file with the following format:

_\_id,title,points,taskcontentpath_

# id
Integer

#title
title of the task

#taskcontentpath
en fil med beskrivelsen av oppgaven

#text
+ HTML without:
- \<html\>
- \<head\>
- \<body\>
- \<script\>-tags.
+ bootstrap3 formatting-classes

#JSON
endpoints return these as json:

task

tasks

usertotalpoints

taskstate

Delivery through Dropbox -> use the username from geekevents. (private browser if needed)
