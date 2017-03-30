import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename

# Initialize the Flask application
app = Flask(__name__)
taskid=''
partid=''
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
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
    return render_template('upload.html', taskid=taskid,partid=partid)




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
        return render_template('success.html', taskid=taskid, partid=partid)
    # return render_template('upload.html')
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
