from flask import request
import os
from werkzeug.utils import secure_filename
from pathlib import Path
from app import app
from datetime import date
import db_operations




def parse_db_content():
    all_rows = db_operations.get_all_rows()
    list_of_rows = []
    current_dict = {}
    for row in all_rows:
        current_dict["id"] = row.id 
        current_dict["filename"] = row.filename
        current_dict["date"] = row.date
        current_dict["extension"] = row.extension
        current_dict["size"] = row.size
        list_of_rows.append(current_dict)
        current_dict = {}

    
    #print(list_of_rows, flush=True)
    return list_of_rows


def buildPackage(id):
    row = db_operations.getElementByID(id)
    response = {}
    response_list = []
    print("buildpackage", flush=True)
    response["id"] = row.id
    response["filename"] = row.filename
    response["date"] = row.date
    response["extension"] = row.extension
    response["size"] = row.size
    print(response, flush=True)
    response_list.append(response)
    return response_list

    

def parsePackage(data):
    filename = data["filename"]
    return filename

def load_File(file, filename):
    #filename = secure_filename(filename)
    print(filename, flush=True)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

def upload(file):
    uploaded_file = file.filename
    now = date.today()
    filename = uploaded_file
    extension = uploaded_file.split(".")[-1]
    checkName = db_operations.checkIfFileNameExists(filename)
    if checkName:
        db_operations.insert(filename, now, extension, size=0)
    else:
        newFileName = db_operations.extendFileName(filename)
        filename = newFileName
        db_operations.insert(filename, now, extension, size=0)
    load_File(file, filename)
    path = "/app/saved_files/" + filename
    file_size = os.stat(path).st_size
    print(file_size, flush=True)
    db_operations.update_size(filename, file_size)
    current_row = db_operations.get_row_by_filename(filename)
    return current_row.id

def rename_static_file(old_filename, new_filename):
    src = "/app/saved_files/" + old_filename
    dst = "/app/saved_files/" + new_filename
    os.rename(src, dst)

def rename(data, id):
    new_filename = parsePackage(data)
    old_filename = db_operations.get_filename(id)
    final_name = db_operations.updateFileName(id, new_filename)
    rename_static_file(old_filename, final_name)
    return final_name

def download(id):
    filename = db_operations.get_filename(id)
    #directory = "/app/saved_files"
    return filename



def delete(id):
    filename = db_operations.get_filename(id)
    db_operations.deleteRow(id)
    path = "/app/saved_files/"
    full_path = path + filename
    searched_file = Path(full_path)
    print(full_path, flush=True)
    if os.path.exists(searched_file):
        print("hat geklappt", flush=True)
    else:
        print("hat nicht geklappt", flush=True)
    os.remove(searched_file)








   