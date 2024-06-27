from db import db

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url =  db.Column(db.String(200), nullable=False)
    in_stock = db.Column(db.Boolean, default=True, nullable=True)

    def __init__(self, name, description, price, image_url, in_stock=True):
        self.name = name
        self.description = description
        self.price = price
        self.image_url = image_url
        self.in_stock = in_stock

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, food_id):
        return cls.query.get(food_id)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'in_stock': self.in_stock
        }
    
    def __repr__(self):
        return f"Food('[{self.id}]:{self.name}')"

    

