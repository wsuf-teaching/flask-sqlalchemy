from flask import Flask
from flask_migrate import Migrate
from db import db
from models.food import Food

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///I://flaskdbproject1//data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

app = create_app()
migrate = Migrate(app, db)
with app.app_context():
    print("Tables loaded and initialised")
    db.create_all()

@app.route('/')
def index():
    return 'Hello, World!'

def seed():
    food1 = Food(name="Pizza", description="Dish of italian origin",price=10.99,image_url="image1.jpg")
    food2 = Food(name="Hamburger", description='Meat and vegetables in a bun', price=15.99, image_url='image2.jpg')
    food3 = Food(name='Sushi', description='Raw fish in rice', price=12.99, image_url='image3.jpg')
    food4 = Food(name='Pasta', description='Italian dish of noodles', price=11.99, image_url='image4.jpg')
    food5 = Food(name='Steak', description='Roasted meat', price=20.99, image_url='image5.jpg')
    food6 = Food(name='Pho', description='Vietnamese noodle soup', price=9.99, image_url='image6.jpg')
    food7 = Food(name='Tacos', description='Mexican dish of tortilla and meat', price=8.99, image_url='image7.jpg')
    food8 = Food(name='Ramen', description='Japanese noodle soup', price=11.99, image_url='image8.jpg')
    food9 = Food(name='Curry', description='Indian dish of meat and vegetables', price=12.99, image_url='image9.jpg')
    food10 = Food(name='Donuts', description='American dessert', price=5.99, image_url='image12.jpg')

    db.session.add_all([food1, food2, food3, food4, food5, food6, food7, food8, food9, food10])

    db.session.commit()

    return 'Seeded data'

if __name__ == '__main__':
    app.run()




