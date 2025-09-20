# app/api/authentication.py
from flask import Blueprint, request, jsonify, current_app
from flask_security import auth_required, current_user, login_user, logout_user
from flask_security.utils import verify_password, hash_password
from app.models.models import User, db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and verify_password(data['password'], user.password):
        login_user(user)
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200

    return jsonify({'error': 'Invalid credentials'}), 401


@auth_bp.route('/api/logout', methods=['POST'])
@auth_required()
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


@auth_bp.route('/api/me', methods=['GET'])
@auth_required()
def get_current_user():
    return jsonify({
        'user': current_user.to_dict()
    }), 200


@auth_bp.route('/api/register', methods=['POST'])
def register():
    from flask_security import current_app
    # Only allow registration if enabled in config
    if not current_app.config.get('SECURITY_REGISTERABLE', False):
        return jsonify({'error': 'Registration is disabled'}), 403

    data = request.get_json()

    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'error': 'Username, email and password required'}), 400

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400

    # Get user_datastore from flask_security
    user_datastore = current_app.extensions['security'].datastore

    # Create user with 'user' role
    user = user_datastore.create_user(
        username=data['username'],
        email=data['email'],
        password=hash_password(data['password'])
    )
    user_datastore.add_role_to_user(user, 'user')

    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201