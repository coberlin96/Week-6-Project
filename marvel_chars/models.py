from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Secrets Module (Given by Python)
import secrets

# Imports fo Flask_login
from flask_login import LoginManager, UserMixin

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db = SQLAlchemy()


# User class goes here
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_create = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'owner, lazy = True')

# __init__, set_token, set_id, set_password, __repr__
    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database"

# Character class goes here
class Character(db.Model):
    id = db.Column(db.String, primary_key=True)
    primary_name = db.Column(db.String(100))
    secret_identity = db.Column(db.String(100))
    aliuses = db.Column(db.String(200))
    description = db.Column(db.String(200))
    first_appearance = db.Column(db.String(150))
    comics_appeared_in = db.Column(db.Numeric(precision=10, scale=0))
    abilities = db.Column(db.String(200))
    original_creator = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    owner_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, primary_name, secret_identity, aliuses, description, first_appearance, comics_appeared_in, abilities, original_creator, owner_token):
        self.id = self.set_id()
        self.primary_name = primary_name
        self.secret_identity = secret_identity
        self.aliuses = aliuses
        self.description = description
        self.first_appearance = first_appearance
        self.comics_appeared_in = comics_appeared_in
        self.abilities = abilities
        self.original_creator = original_creator
        self.owner_token = owner_token

    def __repr__(self):
        return f"The following character entery has been added: {self.primary_name}"

    def set_id(self):
        return(secrets.token_urlsafe())

# CharSchema goes ehre

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ['id', 'primary_name', 'secret_identity', 'aliuses', 'description', 'first_appearance', 'comics_appeared_in', 'abilities', 'original_creator']
    
char_schema = CharacterSchema()
chars_schema = CharacterSchema(many = True)
