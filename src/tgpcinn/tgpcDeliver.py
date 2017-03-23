#!python2
from flask import Flask, json, jsonify, Response, request, abort
from functools import wraps
import csv, codecs, os
from werkzeug.utils import secure_filename

## http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

#uploads
UPLOAD_FOLDER = '../upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py', 'go', 'c', 'sh', 'cpp', 'make',])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)
key = '42'
# read the directories

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree



def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.args.get('key') and request.args.get('key') == key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/tgpcdeliver', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''



@app.route('/tgpcdeliver/api/delivery/', methods=['GET', 'POST'])
@require_appkey
def delivery():
    id=request.args.get('_id')


@app.route('/tgpcdeliver/api/getpoints/')
@require_appkey
def getpoint():
    id=request.args.get('_id')



if __name__ == '__main__':
    app.run()
