from app import db
from Models import Files


def insert(name, date, extension, size):
    print("Inserting", flush=True)
    row = Files(filename=name, date=date, extension=extension, size=size)
    db.session.add(row)
    db.session.commit()

def update_size(filename, size):
    row = Files.query.filter_by(filename=filename).first()
    row.size = size
    db.session.commit()

def checkIfFileNameExists(filename):
    print(filename, flush=True)
    query_for_existing_filename = Files.query.filter_by(filename=filename).first()
    
    if query_for_existing_filename:
        return False
    else: 
        return True
        
    
def extendFileName(filename):
    name_without_extensions = filename.split(".")[0]
    extension = filename.split(".")[1]
    name_list = Files.query.filter(Files.filename.like(name_without_extensions + '%')).all()

    #print(name_list, flush=True)
    fileNames = []
    for row in name_list:
        fileNames.append(row.filename)
    #print(fileNames, flush = True)
    new_name = ""
    checking = True
    i = 1
    while checking:
        new_name = name_without_extensions + " (" + str(i) + ")" + "." + extension
        if new_name  not in fileNames:
            checking = False
        i = i +1

    return new_name

def checkIfIdExists(id):
    query_for_id = Files.query.filter_by(id=id).first()
    print(query_for_id, flush=True)

def updateFileName(id, new_file_name):
    check = checkIfFileNameExists(new_file_name)
    final_name = new_file_name
    if check == False:
        print("in if block", flush=True)
        final_name = extendFileName(new_file_name)
    row = getElementByID(id)
    row.filename = final_name
    db.session.commit()
    print("updated filename", flush=True)
    return final_name

def getElementByID(id):
    row = Files.query.get(id)
    return row

def deleteRow(id):
    row = getElementByID(id)
    print(row, flush=True)
    db.session.delete(row)
    db.session.commit()
    print("deleted row", flush=True)

def get_filename(id):
    row = getElementByID(id)
    print("hiiiiiiiiier", flush=True)
    print(id, flush=True)
    print(row, flush=True)
    filename = row.filename
    return filename

def get_all_rows():
    all_rows = Files.query.all()
    return all_rows

def get_row_by_filename(filename):
    row = Files.query.filter_by(filename=filename).first()
    return row





