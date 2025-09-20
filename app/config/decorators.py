from functools import wraps
from flask import request, jsonify
from app.models.models import User


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]

        if not token and request.args.get('token'):
            token = request.args.get('token')

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        user = User.verify_auth_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401

        request.current_user = user
        return f(*args, **kwargs)

    return decorated_function