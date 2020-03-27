from flask import Flask, request, jsonify
import pprint
import os
import boto3

UPLOAD_FOLDER = './downloads/'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'pdf', 'jpg', 'png', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/conversion-json', methods=["POST", "GET"])
def upload():
    output = {}
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file and allowed_file(file.filename):
        file2 = file
        output["1. name"] = file.filename
        output["2. size"] = file.tell()
        output["3. mimetype"] = file.mimetype
        output["4. extension"] = '.' in file.filename and file.filename.rsplit('.', 1)[1].lower()
        output["5. content"] = file.read().decode("utf-8", errors = 'ignore')
        s3_client = boto3.resource('s3')
        s3_client.Object('monbucketty', file.filename).put (Body = output["5. content"] )
        #filefors3 = s3_client.Object('monbucketty', file.filename)
        #filefors3.put(Body = output["5. content"])
        #s3_client.upload_fileobj(file2, "monbucketty", file.filename)
        return output
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, csv, pdf, jpg, png, jpeg and gif'})
        resp.status_code = 400
        return resp
