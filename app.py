from flask import Flask
from views import init_routes
from flask import render_template, request, redirect, url_for, flash
from models import db

# Create the Flask app and configure it
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise the database and routes
db.init_app(app)
init_routes(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)