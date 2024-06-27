from db import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(20), nullable=False)
    orders = db.relationship('Order', backref='address', lazy=True)

    def json(self):
        return {
            'id': self.id,
            'street': self.street,
            'city': self.city,
            'zip': self.zip
        }