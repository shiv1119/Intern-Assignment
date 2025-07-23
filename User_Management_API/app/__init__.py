from flask import Flask
from app.db.connection import get_db

def create_app(testing=False):
    app = Flask(__name__)

    # Initialising db once so that it can we used throughout the project easily
    app.db = get_db()

    # Registering all the blueprints for simple use
    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    return app

from flask import Flask
from app.db.connection import get_db

def create_app(testing=False):
    app = Flask(__name__)
    
    if testing:
        app.config['TESTING'] = True
        app.config['DATABASE'] = ':memory:' 
    else:
        app.config['DATABASE'] = 'your_prod_or_dev_db.db'

    # Initialising db once so that it can we used throughout the project easily
    app.db = get_db(app.config['DATABASE'])

    # Register Blueprints
    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    return app
