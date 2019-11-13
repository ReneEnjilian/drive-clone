from app import db

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), unique=True, nullable=False)
    date = db.Column(db.String(80), nullable=False)
    extension = db.Column(db.String(80), nullable=False)
    size = db.Column(db.Integer, nullable=False)