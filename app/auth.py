# app/auth.py
from flask_security.utils import hash_password
from app.models.models import db


def create_default_roles_and_admin(user_datastore, cfg):
    """Create default roles and admin users if they don't exist"""
    
    # Create roles if they don't exist
    _create_default_roles(user_datastore)
    
    # Create admin users if they don't exist
    _create_admin_user(user_datastore, cfg)
    _create_super_admin_user(user_datastore, cfg)
    
    db.session.commit()


def _create_default_roles(user_datastore):
    """Create default user roles"""
    roles = [
        ("admin", "Administrator"),
        ("super_admin", "Super Administrator"),
        ("user", "Regular User")
    ]
    
    for role_name, role_description in roles:
        if not user_datastore.find_role(role_name):
            user_datastore.create_role(name=role_name, description=role_description)


def _create_admin_user(user_datastore, cfg):
    """Create admin user if not exists"""
    admin_email = cfg.get('admin.email')
    admin_username = cfg.get('admin.username')
    admin_password = cfg.get('admin.password')

    if not user_datastore.find_user(email=admin_email):
        admin_user = user_datastore.create_user(
            email=admin_email,
            username=admin_username,
            password=hash_password(admin_password)
        )
        user_datastore.add_role_to_user(admin_user, 'admin')
        
        print(f"Admin user created: {admin_username}")



def _create_super_admin_user(user_datastore, cfg):
    """Create super admin user if not exists"""
    super_admin_email = cfg.get('super_admin.email')
    super_admin_username = cfg.get('super_admin.username')
    super_admin_password = cfg.get('super_admin.password')

    if not user_datastore.find_user(email=super_admin_email):
        super_admin_user = user_datastore.create_user(
            email=super_admin_email,
            username=super_admin_username,
            password=hash_password(super_admin_password)
        )
        user_datastore.add_role_to_user(super_admin_user, 'super_admin')
        
        print(f"Super admin user created: {super_admin_username}")
