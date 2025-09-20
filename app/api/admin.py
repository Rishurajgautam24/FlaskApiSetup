# app/api/admin.py
from flask import Blueprint, jsonify, request, current_app
from flask_security import auth_required, roles_required, current_user
from app.models.models import User, Role, db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/users', methods=['GET'])
@auth_required()
@roles_required('admin', 'super_admin')
def get_all_users():
    users = User.query.all()
    return jsonify({
        'users': [user.to_dict() for user in users]
    }), 200


@admin_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@auth_required()
@roles_required('admin', 'super_admin')
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    # Only super admins can assign super_admin role
    if 'roles' in data:
        if 'super_admin' in data['roles'] and not current_user.has_role('super_admin'):
            return jsonify({'error': 'Only super admins can assign super_admin role'}), 403

    # Update user fields
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'active' in data:
        user.active = data['active']

    # Update roles
    if 'roles' in data:
        user_datastore = current_app.extensions['security'].datastore
        user_datastore.set_roles(user, data['roles'])

    db.session.commit()

    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200


@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@auth_required()
@roles_required('super_admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # Prevent self-deletion
    if user.id == current_user.id:
        return jsonify({'error': 'Cannot delete your own account'}), 400

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200