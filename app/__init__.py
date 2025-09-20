# app/__init__.py
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore

from app.config.config import Configuration
from app.models.models import db, User, Role
from app.extensions import init_extensions
from app.auth import create_default_roles_and_admin

# Initialize extensions
security = Security()


def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    configure_app(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Setup security
    setup_security(app)
    
    # Register blueprints
    register_blueprints(app)
    
    return app


def configure_app(app):
    """Configure Flask app with settings"""
    cfg = Configuration()
    
    # Core Flask settings
    app.config['SECRET_KEY'] = cfg.ENV.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = cfg.DATABASE.URL or 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Flask-Security settings
    app.config['SECURITY_PASSWORD_SALT'] = cfg.get('security.password_salt')
    app.config['SECURITY_REGISTERABLE'] = cfg.get('security.registerable')
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = cfg.get('security.send_register_email')
    app.config['SECURITY_USERNAME_ENABLE'] = cfg.get('security.username_enable')
    app.config['SECURITY_USERNAME_REQUIRED'] = cfg.get('security.username_required')
    
    # Cookie security settings
    app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
    app.config["SESSION_COOKIE_SAMESITE"] = "strict"


def setup_security(app):
    """Setup Flask-Security with user datastore"""
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)
    
    # Create tables and default data
    with app.app_context():
        db.create_all()
        cfg = Configuration()
        create_default_roles_and_admin(user_datastore, cfg)


def register_blueprints(app):
    """Register all application blueprints"""
    from app.api.authentication import auth_bp
    from app.api.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/api')