from flask import Blueprint, request, jsonify
from marvel_chars.helpers import token_required
from marvel_chars.models import db, User, Character, char_schema, chars_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route(('/getdata'))
@token_required
def getdata(current_user_token):
    return {'some':'value'}


# Create new character endpoint
@api.route('/chars', methods = ['POST'])
@token_required
def create_char(current_user_token):
    primary_name = request.json['primary_name']
    secret_identity = request.json['secret_identity']
    aliuses = request.json['aliuses']
    description = request.json['description']
    first_appearance = request.json['first_appearance']
    comics_appeared_in = request.json['comics_appeared_in']
    abilities = request.json['abilities']
    original_creator = request.json['original_creator']
    owner_token = current_user_token.token
    
    print(f"BIG TESTER: {current_user_token.token}")

    char = Character(primary_name, secret_identity, aliuses, description, first_appearance, comics_appeared_in, abilities, original_creator, owner_token = owner_token)

    db.session.add(char)
    db.session.commit()

    response = char_schema.dump(char)

    return jsonify(response)

# Retrieve all characters files made by user based on token
@api.route('/chars', methods = ['GET'])
@token_required
def get_chars(current_user_token):
    owner = current_user_token.token
    chars = Character.query.filter_by(owner_token = owner).all()
    response = chars_schema.dump(chars)
    return jsonify(response)

# Retrieve individual character file
@api.route('/chars/<id>', methods = ['GET'])
@token_required
def get_char(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        char = Character.query.get(id)
        response = char_schema.dump(char)
        return jsonify(response)
    else:
        return jsonify({'message': "Valid Token Required"}), 401

# Modify specific character file
@api.route('/chars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_char(current_user_token, id):
    char = Character.query.get(id)

    char.primary_name = request.json['primary_name']
    char.secret_identity = request.json['secret_identity']
    char.aliuses = request.json['aliuses']
    char.description = request.json['description']
    char.first_appearance = request.json['first_appearance']
    char.comics_appeared_in = request.json['comics_appeared_in']
    char.abilities = request.json['abilities']
    char.original_creator = request.json['original_creator']
    char.owner_token = current_user_token.token

    db.session.commit()
    response = char_schema.dump(char)
    return jsonify(response)

# Delete specified character file
@api.route('/chars/<id>', methods = ['DELETE'])
@token_required
def delete_char(current_user_token, id):
    char = Character.query.get(id)
    db.session.delete(char)
    db.session.commit()
    response = char_schema.dump(char)
    return jsonify(response)
