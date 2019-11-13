from app import app
from flask import request, Blueprint, send_from_directory, jsonify, abort
routes = Blueprint("routes", __name__)
import db_operations 
import parser

@app.route("/")
def hello():
    return "this is my file uploader"

@app.route("/getdata", methods=['GET', 'POST'])
def getData():
    complete_data = parser.parse_db_content()
    return jsonify(complete_data)

@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['file']
    id = parser.upload(file)
    response = parser.buildPackage(id)
    return jsonify(response)

#diese routes benötigen try-catch --> falls files nicht mehr verfügbar

@app.route("/download/<int:id>", methods=['GET'])
def download(id):
    try:
        filename = parser.download(id)
    except AttributeError:
        return abort(400)
    print(filename, flush=True)
    print(app.config['UPLOAD_FOLDER'], flush=True)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filename)

@app.route("/rename/<int:id>", methods=['POST'])
def rename(id):
    response = {}
    response["success"] = True
    response["new_filename"] = ""
    data = request.json
    print(data["filename"], flush=True)
    try:
        new_filename = parser.rename(data, id)
        response["new_filename"] = new_filename
    except Exception:
        print("error!!!!!!!", flush=True)
        response["success"] = False
    return jsonify(response)

@app.route("/delete/<int:id>", methods=['DELETE'])
def delete(id):
    response = {}
    response["success"] = True
    try:
        parser.delete(id)
    except:
        response["success"] = False
    print(response, flush=True)
    return jsonify(response)