from flask_sqlalchemy import SQLAlchemy
from db import db

class OrderFood(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    food = db.relationship('Food', backref='order_foods')

    def __init__(self, order_id, food_id, amount):
        self.order_id = order_id
        self.food_id = food_id
        self.amount = amount

    def json(self):
        return {
            'order_id': self.order_id,
            'food_id': self.food_id,
            'amount': self.amount,
            'food': self.food.json()
        }
    
    def __repr__(self):
        return f"OrderFood('{self.order_id}', '{self.food_id}', '{self.amount}')"