from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from ..modules.models import Users
from ..modules.services import save, delete

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/users', methods=['GET', 'POST'])
@jwt_required()
def get_users():

    if request.method == 'POST':

        data = request.get_json()

        new_user = Users(
                        username=data['username'],
                        email=data['email'],
                        )
        
        new_user.set_password(data['password'])

        save(new_user)
        return jsonify({'message': 'User created successfully'}), 201
    
    users = Users.query.all()
    
    return jsonify([user.to_dict() for user in users]), 200


@admin_bp.route('/users/update/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):

    data = request.get_json()
    user = Users.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data and data['password']:
        user.set_password(data['password'])

    save(user)

    return jsonify({'message': 'User updated successfully'}), 200


@admin_bp.route('/users/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):

    user = Users.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    delete(user)
    return jsonify({'message': 'User deleted successfully'}), 200


@admin_bp.route('/login', methods=['POST'])
def login():
        
    data = request.get_json()
    user = Users.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):

        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return jsonify({ 'access_token': access_token, 'refresh_token': refresh_token }), 200
        
    
    return jsonify({'message': 'Invalid username or password'}), 401
