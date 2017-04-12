# -*- coding: utf-8 -*-
from flask import Flask, json, jsonify, Response, request, abort
from functools import wraps
from tempfile import mkstemp
from shutil import move
from os import close, remove
import os, requests

import csv, codecs
app = Flask(__name__)


tasksdone = open('tasksdone.txt','rbU') #taskname, partids
ord=open('tasks/ord.txt', 'rbU')
csvfile =open('tasks/tasks.txt', 'rbU')

rows=[]
i=0
#4,2048,"et morsomt spill",src/tasks/2048.txt
fieldnames = ("_id", "title", "sum", "teaser", "contenturl")
reader = csv.DictReader(csvfile, fieldnames)
key = '590787712188'
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


@app.route('/tgpc/api/taskstate/<int:partid>/',methods=['GET'])
@require_appkey
def get_taskstate(partid):
    #return the praticipants that have done this task and succeeded.
    # _id, [partids]
    statuslist = []
    f = open("uploads/"+str(partid)+"/deliverd.txt", 'r')
    fields = ("task", "status")
    status_dict = csv.DictReader(f, fields)
    print status_dict
    for row in status_dict:
        statuslist.append(row)
    f.close()
    return jsonify({'taskstate':statuslist})


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
    lb=sorted(participantslist, key=lambda k: k['sum'],reverse=True)
    return jsonify({"leaderboard":lb})

def getpartlist():
    participants = open('uploads/participants.txt','r')
    participantslist=[]
    fields=("partid","partname","sum")
    participantsDict=csv.DictReader(participants, fields)
    for row in participantsDict:
        participantslist.append(row)
    return participantslist

## stotte funskjon
@app.route('/tgpc/api/ord', methods=['GET'])
def serveord():
    ordliste=ord.readlines()
    return Response(ordliste)

@app.route('/tgpc/api/deliver/<int:taskid>', methods=['GET','POST'])
@require_appkey
def deliver(taskid):
    content = request.json
    if not os.path.isdir("uploads/"+content['partid']):
        os.mkdir("uploads/"+content['partid'])
        with open("uploads/participants.txt", 'a') as file:
            file.write(content['partid']+","+content['partname']+",0\n")

    if not os.path.exists("uploads/"+content['partid']+"/"+str(taskid)):
        with open("uploads/"+content['partid']+"/deliverd.txt", 'a+') as file:
            file.write(str(taskid)+",0\n")

    with open("uploads/"+content['partid']+"/"+str(taskid), 'w') as file:
        file.write(content['solution'])

    res = requests.post('http://localhost:5000/tgpc/check/'+str("uploads/"+content['partid']+"/"+str(taskid)+content['lang'])+'?key=123')

    statuses = []
    with open("uploads/"+content['partid']+"/deliverd.txt", 'r') as file:
        statuses = file.readlines()
    
    for i, j in enumerate(statuses):
        if str(taskid)+"," in j:
            statuses[i] = str(taskid)+","+res.text

    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        for i in statuses:
            new_file.write("%s" % i);
    
    close(fh)
    #Remove original file
    remove("uploads/"+content['partid']+"/deliverd.txt")
    #Move new file
    move(abs_path, "uploads/"+content['partid']+"/deliverd.txt")

    return jsonify({'state':'good'})

@app.route('/tgpc/api/deliveries/<int:partid>', methods=['GET'])
@require_appkey
def getdeliveries(partid):
    fieldnames=['taskid', 'state']
    delifile= open("uploads/"+str(partid)+"/deliverd.txt", 'r')
    tasks=csv.DictReader(delifile, fieldnames)
    taskspart=[]
    for row in tasks:
        taskspart.append(row)
    delifile.close()
    return jsonify({"taskspart":taskspart})



if __name__ == '__main__':
    app.run()
