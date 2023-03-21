from flask import Flask,render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.route('/tourist')
    def tourist():
        return render_template('tourist.html')
    @app.route('/local')
    def local():
        return render_template('local.html')
    @app.route('/guide')
    def guide():
        return render_template('guide.html')
    
    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/login')
    def login():
        render_template('login.html')
    
    @app.route('/staff')
    def staff():
        render_template('staff.html')
    
    
        

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

