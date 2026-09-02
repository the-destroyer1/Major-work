from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Basic item info
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    item_type = db.Column(db.String(100), nullable=True)

    # Optional commercial fields
    price = db.Column(db.Float, nullable=True)
    size = db.Column(db.String(100), nullable=True)
    colour = db.Column(db.String(100), nullable=True)

    # Stores the PNG filename from static/images
    images = db.Column(db.String(100), nullable=True)

    # Optional timestamp for sorting or future features
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Item {self.id} - {self.title}>"
