from flask import render_template, request, redirect, url_for, flash, session
from models import db, Item
import os

def init_routes(app):

    @app.route('/')
    def index():
        title = request.args.get("title", "")
        item_type = request.args.get("item_type", "")

        query = Item.query

        if title:
            query = query.filter(Item.title.ilike(f"%{title}%"))
        if item_type:
            query = query.filter(Item.item_type == item_type)

        items = query.all()
        return render_template('index.html', items=items)
    
    @app.route('/gallery')
    def gallery():
        title = request.args.get("title", "")
        item_type = request.args.get("item_type", "")

        query = Item.query

        if title:
            query = query.filter(Item.title.ilike(f"%{title}%"))
        if item_type:
            query = query.filter(Item.item_type == item_type)

        items = query.all()
        return render_template('gallery.html', items=items)

    @app.route('/custom')
    def custom():
        title = request.args.get("title", "")
        item_type = request.args.get("item_type", "")

        query = Item.query

        if title:
            query = query.filter(Item.title.ilike(f"%{title}%"))
        if item_type:
            query = query.filter(Item.item_type == item_type)

        items = query.all()
        return render_template('custom.html', items=items)

    @app.route("/add", methods=["GET", "POST"])
    def add_item():
        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            item_type = request.form.get("item_type")
            price = request.form.get("price")
            size = request.form.get("size")
            colour = request.form.get("colour")
            image = request.form.get("image")

            new_item = Item(
                title=title,
                description=description,
                item_type=item_type,
                price=price,
                size=size,
                colour=colour,
                images=image
            )

            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for("index"))

        images = [
            f for f in os.listdir("static/images")
            if f.lower().endswith(".png")
        ]

        return render_template("add.html", images=images)

    @app.route('/edit/<id>', methods=['GET', 'POST'])
    def edit_item(id):
        item = Item.query.get_or_404(id)

        if request.method == 'POST':
            item.title = request.form['title']
            item.item_type = request.form['item_type']
            item.description = request.form['description']
            item.price = float(request.form['price'])
            item.size = request.form['size']
            item.colour = request.form['colour']
            item.images = request.form['image']

            db.session.commit()
            flash('Item updated successfully!', 'success')
            return redirect(url_for('index'))

        return render_template('edit.html', item=item)

    @app.route('/item/<id>', methods=['GET'])
    def view_item(id):
        item = Item.query.get(id)
        return render_template('item.html', item=item)

    # -----------------------------
    # CART SYSTEM
    # -----------------------------

    @app.route("/add_to_cart/<int:id>", methods=["POST"])
    def add_to_cart(id):
        cart = session.get("cart", [])

        # If item already in cart, increase quantity
        for entry in cart:
            if entry["id"] == id:
                entry["quantity"] += 1
                break
        else:
            cart.append({"id": id, "quantity": 1, "type": "normal"})

        session["cart"] = cart
        flash("Item added to cart.", "success")
        return redirect(request.referrer or url_for("index"))

    @app.route("/cart/update/<id>", methods=["POST"])
    def update_quantity(id):
        cart = session.get("cart", [])
        new_qty = int(request.form["quantity"])

        for entry in cart:
            if str(entry["id"]) == str(id):
                entry["quantity"] = max(1, new_qty)
                break

        session["cart"] = cart
        flash("Quantity updated.", "info")
        return redirect(url_for("cart"))

    @app.route("/cart/remove/<id>", methods=["POST"])
    def remove_from_cart(id):
        cart = session.get("cart", [])
        cart = [entry for entry in cart if str(entry["id"]) != str(id)]
        session["cart"] = cart
        flash("Item removed.", "info")
        return redirect(url_for("cart"))

    @app.route("/cart")
    def cart():
        raw_cart = session.get("cart", [])
        cart_data = []

        # Convert old int-only entries
        for entry in raw_cart:
            if isinstance(entry, int):
                cart_data.append({"id": entry, "quantity": 1, "type": "normal"})
            else:
                cart_data.append(entry)

        session["cart"] = cart_data

        items = []

        for entry in cart_data:

            # Custom item
            if entry.get("type") == "custom":
                class CustomItem:
                    pass
                item = CustomItem()
                item.id = entry["id"]
                item.title = entry["title"]
                item.price = entry["price"]
                item.quantity = entry["quantity"]
                items.append(item)

            # Normal item
            else:
                db_item = Item.query.get(entry["id"])
                if db_item:
                    db_item.quantity = entry["quantity"]
                    items.append(db_item)

        total = sum(i.price * i.quantity for i in items)

        return render_template("cart.html", items=items, total=total)

    # DELETE ITEM

    @app.route('/delete/<int:id>', methods=['POST'])
    def delete_item(id):
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
        return redirect(url_for('index'))

    # CUSTOM ORDER

    @app.route('/create_order', methods=['POST'])
    def create_order():
        blade = request.form.get('blade_type', 'chef')
        handle = request.form.get('handle_material', 'purple_heart')
        length = float(request.form.get('length', 30))
        finish = request.form.get('finish', 'polished')

        base_prices = {'chef':120,'dagger':80,'sword':250,'cleaver':100}
        handle_prices = {'purple_heart':40,'gidgee':55,'teak':30}
        finish_prices = {'polished':0,'brushed':10,'patina':20}

        length_factor = 1 + max(0, (length - 30)) * 0.01
        price = (base_prices[blade] + handle_prices[handle] + finish_prices[finish]) * length_factor

        cart = session.get("cart", [])

        custom_item = {
            "id": f"custom-{blade}-{handle}-{length}-{finish}",
            "type": "custom",
            "title": f"Custom {blade.capitalize()} ({handle.replace('_',' ').title()})",
            "price": round(price, 2),
            "quantity": 1
        }

        # If same custom item exists, increase quantity
        for entry in cart:
            if entry["id"] == custom_item["id"]:
                entry["quantity"] += 1
                break
        else:
            cart.append(custom_item)

        session["cart"] = cart
        flash("Custom blade added to cart!", "success")

        return redirect(url_for("cart"))

    @app.route("/checkout")
    def checkout():
        return render_template("checkout.html")
