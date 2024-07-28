import os 

from flask import Flask

from marshmallow.exceptions import ValidationError

from init import  db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)

    # Turns off default ordering of list
    app.json.sort_keys = False

    # Define configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Import bp from commands
    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)
    # Register bp in flask instance
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.book_controller import book_bp
    app.register_blueprint(books_bp)

    from controllers.wishlist_controller import wishlists_bp
    app.register_blueprint(wishlists_bp)

    from controllers.rating_controller import rating_bp
    app.register_blueprint(rating_bp)

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



