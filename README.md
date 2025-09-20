# Flask Security API

A robust Flask-based REST API with built-in authentication, authorization, and role-based access control using Flask-Security.

## Features

- 🔐 **Authentication**: JWT-based authentication with Flask-Security
- 👥 **Role-Based Access Control**: Admin, Super Admin, and User roles
- 🛡️ **Security**: Password hashing, secure cookies, and CSRF protection
- 📊 **Database**: SQLAlchemy with Flask-Security models
- ⚙️ **Configuration**: YAML-based configuration with environment variable support
- 🔧 **Admin Panel**: Built-in admin user creation and management

## Project Structure

```
flask-project/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py          # Database models (User, Role)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication endpoints
│   │   └── admin.py           # Admin management endpoints
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.yaml
│   │   └── config.py          # Configuration management
│   └── __init__.py            # Application factory
│   └── auth.py   
│   └── extensions.py   
├── main.py                    # Application entry point
├── .env                       # Environment variables (optional)
├── project.toml
├── README.md
├── uv.lock 
└── requirements.txt           # Python dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd flask-project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install uv
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Set up environment variables** (optional)
   ```bash
   # Create .env file
   echo "SECRET_KEY=your-super-secret-key" >> .env
   echo "DATABASE_URL=sqlite:///app.db" >> .env
   ```

## Configuration

Edit `config.yaml` to customize your application:

```yaml
app:
  name: "Flask Security API"
  host: "0.0.0.0"
  port: 5000

env:
  secret_key: "your-super-secret-key"
  debug: true

database:
  url: "sqlite:///app.db"

security:
  password_salt: "your-password-salt"
  registerable: false
  send_register_email: false

admin:
  email: "admin@example.com"
  username: "admin"
  password: "admin123"

super_admin:
  email: "superadmin@example.com"
  username: "superadmin"
  password: "superadmin123"
```

## Usage

### Starting the Application

```bash
python main.py
```

The application will start on `http://localhost:5000`

### Default Admin Users

On first run, the application automatically creates:
- **Admin User**: `admin` / `admin123`
- **Super Admin User**: `superadmin` / `superadmin123`

**⚠️ Change these passwords in production!**


## Security Considerations

1. **Change default passwords** for admin users
2. **Use strong secret keys** in production
3. **Enable HTTPS** in production environments
4. **Set `debug: false`** in production config
5. **Use environment variables** for sensitive data
6. **Regularly update dependencies**

## Environment Variables

The application supports these environment variables:

- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: Database connection URL
- `FLASK_ENV`: Environment (development/production)
- `DEBUG`: Debug mode true/false


## Troubleshooting

### Common Issues

1. **Database not created**: Run `python main.py` once to initialize database
2. **Import errors**: Check your PYTHONPATH and virtual environment
3. **Authentication fails**: Verify user exists in database
4. **Permission errors**: Check user roles and permissions

### Logs

Check application logs for detailed error information:

```bash
tail -f app.log  # If logging is configured
```

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review Flask-Security documentation
3. Check application logs for error details

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Note**: This is a basic implementation. For production use, consider adding:
- Rate limiting
- API documentation (Swagger/OpenAPI)
- Advanced error handling
- Monitoring and logging
- Database backups
- SSL/TLS encryption