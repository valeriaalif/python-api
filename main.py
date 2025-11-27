from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import subprocess


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5433/items'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f'<Item {self.name}>'
    
    @app.route('/items', methods=['POST'])
    def create_item():
        data = request.get_json()
        new_item = Item(name=data['name'], description=data.get('description'))
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item created successfully', 'id': new_item.id}), 201
    
    @app.route('/items', methods=['GET'])
    def get_items():
        items = Item.query.all()
        output = []
        for item in items:
            output.append({'id': item.id, 'name': item.name, 'description': item.description})
        return jsonify({'items': output})
    
    @app.route('/items/<int:item_id>', methods=['PUT'])
    def update_item(item_id):
        item = Item.query.get_or_404(item_id)
        data = request.get_json()
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        db.session.commit()
        return jsonify({'message': 'Item updated successfully'})
    
    @app.route('/items/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
