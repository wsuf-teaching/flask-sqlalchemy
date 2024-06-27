from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')
    orders = db.relationship('Order', backref='user', lazy=True)

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active
    
    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []
    
    def get_custom_claims(self):
        return {
            'name': self.username,
            'age': 66
        }
