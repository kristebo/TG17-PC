from flask import Flask, json, jsonify, Response, request, abort, os
from functools import wraps
from

import csv, codecs
app = Flask(__name__)
key = '42'

#uploads
UPLOAD_FOLDER = 'tg/TG17-PC/src/tgpcinn/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py', 'go', 'c', 'sh', 'cpp', 'make',])

def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


@require_appkey
def newuser():
    partid=request.args.get('id')
    os.makedirs('id')




@app.route('tgpcdeliver/api/delivery/', methods=['GET', 'POST'])
@require_appkey
def delivery():
    id=request.args.get('id')
    partid=request.args.get('pid')
    os.makedirs(id/partid)

@app.route('/tgpc/api/getpoints/')
@require_appkey
def getpoint():
    id=request.args.get('id')
    partid=request.args.get('pid')
        try: lst=os.listdirs()




if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
