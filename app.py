from flask import Flask, request, jsonify
import os, boto3

#l'API accepte les fichiers txt et csv
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)

#fonction qui verifie que le ficher est du bon format
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/conversion-json', methods=["POST", "GET"])
def post():
    output = {}
    #s'il n'y a pas de fichier, on renvoie un message d'erreur
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    #si le fichier et présent et du bon format, on le traite
    if file and allowed_file(file.filename):
        file2 = file
        output["1. name"] = file.filename
        output["2. size"] = file.tell()
        output["3. mimetype"] = file.mimetype
        output["4. extension"] = '.' in file.filename and file.filename.rsplit('.', 1)[1].lower()
        output["5. content"] = file.read().decode("utf-8", errors = 'ignore')
        #enregistrement du fichier sur S3
        s3_client = boto3.resource('s3') #enregistrement sur
        s3_client.Object('monbucketty', file.filename).put (Body = output["5. content"] )
        return output
    #si le fichier est du mauvais format, on renvoie un message d'erreur
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, csv, pdf, jpg, png, jpeg and gif'})
        resp.status_code = 400
        return resp
