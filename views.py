from flask import render_template, request, redirect, url_for, flash
from models import db, Item

def init_routes(app):

    @app.route('/')
    def index():
        title = request.args.get("title", "")
        item_type = request.args.get("item_type", "")

        query = Item.query

        # Apply filters if present
        if title:
            query = query.filter(Item.title.ilike(f"%{title}%"))
        if item_type:
            query = query.filter(Item.item_type == item_type)

        items = query.all()

        return render_template('index.html', items=items)


    @app.route('/add', methods=['GET', 'POST'])
    def add_item():
        if request.method == 'POST':
            new_item = Item(
                title=request.form['title'],
                item_type=request.form['item_type'],
                description=request.form['description'],
                price=float(request.form['price']),
                size=request.form['size'],
                colour=request.form['colour'],
                images=request.form['image']
            )
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully!', 'success')
            return redirect(url_for('index'))

        return render_template('add.html')
    
    @app.route('/edit/<id>', methods=['GET', 'POST'])
    def edit_item(id):
        item = Item.query.get_or_404(id)   # fetch existing item or 404 if not found

        if request.method == 'POST':
            # update existing item instead of creating new one
            item.title = request.form['title']
            item.item_type = request.form['item_type']
            item.description = request.form['description']
            item.price = float(request.form['price'])
            item.size = request.form['size']
            item.colour = request.form['colour']
            item.images = request.form['image']

            db.session.commit()   # no need to add(), just commit changes
            flash('Item updated successfully!', 'success')
            return redirect(url_for('index'))

        return render_template('edit.html', item=item)

    @app.route('/item/<id>', methods=['GET'])
    def view_item(id):
        item = Item.query.get(id)
        return render_template('item.html', item=item)



    @app.route('/delete/<int:id>', methods=['POST'])
    def delete_item(id):
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
        return redirect(url_for('index'))

