from flask import Flask
from marshmallow.exceptions import ValidationError

from init import  db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://booky_dev:123456@localhost:5432/booky_db"
    
    app.config["JWT_SECRET_KEY"] = "secret"

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(400)
    def bad_request(err):
        return {"error": str(err)}, 400
    
    @app.errorhandler(404)
    def not_found(err):
        return {"error": str(err)}, 404
    
    @app.errorhandler(ValidationError)
    def validation_error(error):
        return {"error": error.messages}, 400
    

    return app



