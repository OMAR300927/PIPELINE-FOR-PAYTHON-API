from ..extinsion import db
from werkzeug.security import generate_password_hash, check_password_hash



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'User {self.username}'
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
    

class Players(db.Model):

    from datetime import datetime
    
    player_name = db.Column(db.String(80), primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Player {self.player_name}'
    