from flask import Flask, json, jsonify, Response, request, abort
from functools import wraps

import csv, codecs
app = Flask(__name__)
# [
#          {'number': 1, 'title': title, 'points': points, 'content': contenturl},
#          {'number': 2, 'title': title, 'points': points, 'content': contenturl} 
# 	   ...
#          ]



csvfile = open('tasks.txt', 'r')
rows=[]
i=0
fieldnames = ("_id", "title", "points", "contenturl")
reader = csv.DictReader(csvfile, fieldnames)
key = '24'
print reader
for row in reader:
    rows.append(row)

# For having a key. Do localhost:5000/path/here?key=24
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
            buffer = ""
            with open(row["contenturl"]) as fd:
                buffer = fd.readlines()

            return jsonify({'task_content':buffer})
    abort(404)


@app.route('/tgpc/api/tasks',methods=['GET'])
@require_appkey
def get_tasks():
    return jsonify({'tasks':rows})  #will return the json

if __name__ == '__main__':
    app.run()
