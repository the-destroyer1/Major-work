from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    item_type = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=True)
    size = db.Column(db.String(100), nullable=True)
    colour = db.Column(db.String(100), nullable=True)
    images = db.Column(db.String(100), nullable=True)

