from flask import Flask, jsonify, request
from flask_migrate import Migrate
from db import db
from models.food import Food
from models.user import User
from models.order import Order
from models.orderfood import OrderFood
from models.address import Address

import flask_praetorian
# only use cors in development
import flask_cors

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///I://flaskdbproject1//data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # NEVER put config values like secret key here
    app.config['SECRET_KEY']="blahblahblah"
    app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
    app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
    global guard
    guard = flask_praetorian.Praetorian()
    guard.init_app(app, User)
    # only use cors in development
    cors = flask_cors.CORS()
    cors.init_app(app)
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

@app.route('/foods', methods=['GET'])
def get_all_foods():
    foods = Food.get_all()
    return jsonify([food.json() for food in foods]), 200

@app.route('/food/<int:id>', methods=['GET'])
def get_food_by_id(id):
    food = Food.get_by_id(id)
    # food = Food.query.get(id)
    if food:
        return food.json(), 200
    else:
        return jsonify({"message":"Food not found"}), 404
    
@app.route('/food', methods=['POST'])
def create_food():
    data = request.get_json()
    new_food = Food(
        name=data["name"],
        description=data["description"],
        price=data["price"],
        image_url=data["image_url"]
    )
    db.session.add(new_food)
    db.session.commit()
    return new_food.json(),201

@app.route('/food/<int:id>', methods=['PUT'])
def update_food(id):
    data = request.get_json()
    food = Food.get_by_id(id)
    if food:
        food.name = data.get('name', food.name)
        food.description = data.get('description', food.description)
        food.price = data.get('price', food.price)
        food.image_url = data.get('image_url', food.image_url)
        db.session.commit()
        return jsonify(food.json()),200
    else:
        return jsonify({"message":"Food not found"}), 404
    
@app.route('/food/<int:id>', methods=['DELETE'])
def delete_food(id):
    food = Food.get_by_id(id)
    if food:
        db.session.delete(food)
        db.session.commit()
        return jsonify({"message":"Food successfully deleted"}), 200
    else:
        return jsonify({"message":"Food not found"}), 404

@app.route('/login', methods=['POST'])
def login():
    req = request.get_json(force=True)
    username = req.get('username')
    password = req.get('password')
    user = guard.authenticate(username, password)
    custom_claims = user.get_custom_claims()
    jwt_token = {"access_token":guard.encode_jwt_token(user, sub=user.username, custom_claims=custom_claims)}
    return jwt_token, 200

@app.route('/register', methods=['POST'])
def register():
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    if not username or not password:
        return {"message":"Username and password are required"}, 400
    existing_user = User.lookup(username)
    if existing_user:
        return {"message":"User already exists"}, 400
    user = User(username=username,password=guard.hash_password(password),roles="")
    db.session.add(user)
    db.session.commit()
    return {'message': 'User registered successfully'}, 201

# protected route, authentication (logging in) should be required
@app.route('/protected', methods=['GET'])
@flask_praetorian.auth_required
def protected():
    # "Authorization: Bearer <your_token>"
    return {"message":f"protected endpoint, current logged in user is {flask_praetorian.current_user().username}"}

# admin only route
@app.route('/adminonly', methods=['GET'])
@flask_praetorian.roles_required("admin")
def admin_route():
    return {"message":f"admin only endpoint, current logged in user is {flask_praetorian.current_user().username}"}

@app.route('/orders')
def get_order():
    orders = Order.get_all()
    return jsonify([order.json() for order in orders])

@app.route('/myorders')
@flask_praetorian.auth_required
def get_my_orders():
    userid = flask_praetorian.current_user_id()
    orders = Order.get_by_user_id(userid)
    return jsonify([order.json() for order in orders])

@app.route('/order', methods=['POST'])
@flask_praetorian.auth_required
def new_order():
    req = request.get_json(force=True)

    street = req.get('street')
    city = req.get('city')
    zip_code = req.get('zip')

    items = req.get('items', [])
    if not items:
        return jsonify({"error": "No items in order"}), 400
    
    food_ids = [item['id'] for item in items]
    existing_foods = Food.query.filter(Food.id.in_(food_ids)).all()
    existing_food_ids = {food.id for food in existing_foods}

    for item in items:
        if item['id'] not in existing_food_ids:
            return jsonify({"error": f"Food id {item['id']} does not exist"}), 400
        
    new_address = Address(street=street, city=city, zip=zip_code)
    db.session.add(new_address)
    db.session.commit()

    user = flask_praetorian.current_user()
    new_order = Order(user_id=user.id, address_id=new_address.id)
    db.session.add(new_order)
    db.session.commit()

    for item in items:
        order_food = OrderFood(order_id=new_order.id, food_id=item['id'], amount=item['amount'])
        db.session.add(order_food)

    db.session.commit()

    return jsonify({"message": "Order created successfully"}), 201


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

#def seed2():
#    user = User(username="admin@example.com",password=guard.hash_password("12345"),roles="admin")
#    db.session.add(user)
#    db.session.commit()

if __name__ == '__main__':
    app.run()




