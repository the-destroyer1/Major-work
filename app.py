from flask import Flask, render_template, request, redirect, url_for, flash, session
from views import init_routes
from models import db
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

IMAGE_FOLDER = "static/images"

db.init_app(app)
init_routes(app)

# -----------------------------
# PNG SELECTOR ROUTES ONLY
# -----------------------------

@app.route("/select")
def select_image():
    images = [
        f for f in os.listdir(IMAGE_FOLDER)
        if f.lower().endswith(".png")
    ]
    return render_template("select.html", images=images)

@app.route("/use-image/<int:item_id>", methods=["POST"])
def use_image(item_id):
    filename = request.form.get("filename")

    if not filename:
        flash("No image selected.")
        return redirect(url_for("select_image"))

    from models import Item
    item = Item.query.get_or_404(item_id)
    item.images = filename
    db.session.commit()

    flash(f"Updated item {item.title} with image {filename}")
    return redirect(url_for("edit_item", item_id=item_id))

# -----------------------------
# Run the app
# -----------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
