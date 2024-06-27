from flask_sqlalchemy import SQLAlchemy
from db import db
from models.address import Address

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_foods = db.Relationship('OrderFood', backref="order", lazy=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id', name='fk_order_address'), nullable=True)

    def __init__(self, user_id, address_id):
        self.user_id = user_id
        self.address_id = address_id

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, order_id):
        return cls.query.get(order_id)

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()   

    def json(self):
        address = Address.query.get(self.address_id)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'address': address.json() if address else None,
            'order_foods': [order_food.json() for order_food in self.order_foods]
        }

    def __repr__(self):
        return f"Order('Order#{self.id} belonging to User#{self.user_id}')"