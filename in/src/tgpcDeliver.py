import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename

app = Flask(__name__)
taskid=''
partid=''

app.config['UPLOAD_FOLDER'] = 'src/uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'c', 'py', 'php', 'htm', 'html', 'go', 'sh'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
# summary = request.args.get('summary', None) # use default value repalce 'None'
# "localhost:5000/tgpc/api/?taskid=id&partid=id

@app.route('/tgpc/api')
def upload():
    taskid=request.args.get('taskid', type=str)
    partid=request.args.get('partid', type=str)
    return render_template('upload.html', taskid=taskid, partid=partid)




# Route that will process the file upload
@app.route('/tgpc/upload', methods=['POST', 'GET'])
def upload_file():
    # Get the name of the uploaded file
    taskid=request.args.get('taskid',type=str)
    partid=request.args.get('partid',type=str)
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(repr(partid)+'_'+repr(taskid)+"_"+file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return render_template('success.html',taskid=taskid, partid=partid)
    else:
        return render_template('failure.html', filename=filename)
