# app/models/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_security.models import fsqla_v3 as fsqla

# Initialize SQLAlchemy
db = SQLAlchemy()

# Set up Flask-Security models
fsqla.FsModels.set_db_info(db)


class Role(db.Model, fsqla.FsRoleMixin):
    """Role model for user permissions"""
    __tablename__ = 'role'

    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model, fsqla.FsUserMixin):
    """User model with authentication support"""
    __tablename__ = 'user'

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active,
            'roles': [role.name for role in self.roles],
            'created_at': self.create_datetime.isoformat() if self.create_datetime else None
        }

    def has_role(self, role_name):
        """Check if user has specific role"""
        return any(role.name == role_name for role in self.roles)

    def is_admin(self):
        """Check if user is admin or super_admin"""
        return any(role.name in ['admin', 'super_admin'] for role in self.roles)

    def is_super_admin(self):
        """Check if user is super_admin"""
        return self.has_role('super_admin')