# main.py
from app import create_app

app = create_app()

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(
        # host=app.config.get('HOST', '0.0.0.0'),
        # port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )