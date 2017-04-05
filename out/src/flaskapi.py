
# -*- coding: utf-8 -*-
from flask import Flask, json, jsonify, Response, request, abort
from functools import wraps

import csv, codecs
app = Flask(__name__)


tasksdone = open('tasksdone.txt','rbU') #taskname, partids
ord=open('tasks/ord.txt', 'rbU')
csvfile =open('tasks/tasks.txt', 'rbU')

rows=[]
i=0
#4,2048,"et morsomt spill",src/tasks/2048.txt
fieldnames = ("_id", "title", "teaser", "contenturl")
reader = csv.DictReader(csvfile, fieldnames)
key = '24'
print reader
for row in reader:
    rows.append(row)

# For having a key. Do host:5000/path/here?key=24
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

@app.route('/index')
@app.route('/')
def make_hello():
    return "glalalla"


@app.route('/tgpc/api/gettask/<int:taskid>/', methods=['GET'])
@require_appkey
def gettask(taskid):
    for row in rows:
        if int(row["_id"]) == taskid:
            jsondata=""
            jsondata=json.load(open(row["contenturl"]))
            for key in jsondata:
                print jsondata.get(key)
            return jsonify({"taskcontent":jsondata})
    abort(404)

## /tgpc/api/tasks?partid=partid
@app.route('/tgpc/api/tasks/',methods=['GET'])
@require_appkey
def get_tasks():
    partid=request.args.get('partid')
    rtasks=[]
    taskdone=[]
    fieldsr=('_id', 'taskname', 'partids')
    print partid
    rowstaski=csv.DictReader(taskdone, fieldsr)
    for rowsi in rowstaski:
        rtasks.append(rowsi)
    for d in rtasks:
        if partid in d.get('partids'):
            print partid
            taskdone.append(d)
            print partid
            return jsonify({'tasksdone':taskdone})  #will return the json
    return jsonify({'tasks':rows})


@app.route('/tgpc/api/taskstate/<int:tasknr>/',methods=['GET'])
@require_appkey
def get_taskstate(tasknr):
    #return the praticipants that have done this task and succeeded.
    # _id, [partids]
    rowstask=[]
    fieldst=("taskname", "participants")
    rowstaskt=csv.DictReader(tasksdone, fieldst)
    for row in rowstaskt:
        rowstask.append(row)
    return jsonify({'taskstate':rowstask[tasknr-1]})


@app.route('/tgpc/api/parttotal/<partid>')
@require_appkey
def get_participant_total(partid):
    participantslist=getpartlist()
    for p in participantslist:
        if p.get('partid')==partid:
            return jsonify({'participant':p})
    return -1

## TODO: bygg leader board.
@app.route('/tgpc/api/leaderboard')
@require_appkey
def get_leader_board():
    participantslist=getpartlist()
    lb=sorted(participantslist, key=lambda k: int(k['sum']),reverse=True)
    return jsonify({"leaderboard":lb})

def getpartlist():
    participants = open('participants.txt','r')
    participantslist=[]
    fields=("partid","partname","sum")
    participantsDict=csv.DictReader(participants, fields)
    for row in participantsDict:
        participantslist.append(row)
    return participantslist

## stotte funskjon
@app.route('/tgpc/api/ord')
def serveord():
    ordliste=ord.readlines()
    return Response(ordliste)


if __name__ == '__main__':
    app.run()
