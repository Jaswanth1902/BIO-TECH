from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user') # admin, lab, farmer, processor, regulator, consumer

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(64), unique=True, index=True, nullable=False)
    batch_type = db.Column(db.String(64), nullable=False) # food, herb, sample
    name = db.Column(db.String(128), nullable=False)
    origin = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    blockchain_tx_hash = db.Column(db.String(66), nullable=True) # tx hash for batch creation
    
    events = db.relationship('Event', backref='batch', lazy='dynamic')
    documents = db.relationship('Document', backref='batch', lazy='dynamic')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'), index=True, nullable=False)
    event_type = db.Column(db.String(64), nullable=False) # collection, transport, storage, test, package, dispose
    location = db.Column(db.String(128))
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    remarks = db.Column(db.Text)
    blockchain_tx_hash = db.Column(db.String(66), nullable=True)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'), index=True, nullable=False)
    doc_type = db.Column(db.String(64), nullable=False) # lab_report, certificate, export_doc
    file_path = db.Column(db.String(256), nullable=False)
    file_hash = db.Column(db.String(64), nullable=False) # hash for integrity
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
