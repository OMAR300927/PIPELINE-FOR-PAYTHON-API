from flask import Flask, redirect
# if you use don't used .env file you can set the config like this, and define them in your server environment variables
# import os
# from dotenv import load_dotenv
# load_dotenv()
# SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
# JWT_SECRET_KEY = os.getenv('SECRET_KEY')
# SECRET_KEY = os.getenv('SECRET_KEY')



# to make gunicorn see the variables in .env file
from dotenv import load_dotenv


load_dotenv()


def create_app():

    app = Flask(__name__)
    app.config.from_prefixed_env()

    from .extinsion import db, migrate, jwt

    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)

    from .Admin.route import admin_bp
    from .Users.route import user_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return redirect('/users')

    return app