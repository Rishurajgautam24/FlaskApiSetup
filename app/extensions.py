# app/extensions.py
"""
Flask extensions initialization module.
Centralizes all extension setup for better organization.
"""

from app.models.models import db


def init_extensions(app):
    """Initialize Flask extensions with the app"""
    # Initialize SQLAlchemy
    db.init_app(app)