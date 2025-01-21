from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os





db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)


    #db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:23hellboundFRENZY@localhost:3306/tacorp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #file upload handling
    UPLOAD_FOLDER = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    #pass app as argument
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    from myapp.routes import routes
    app.register_blueprint(routes)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    return app



