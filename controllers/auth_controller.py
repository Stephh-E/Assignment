from flask import Blueprint, request

from init import bcrypt, db
from models.user import User, user_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_bp.route("/register", methods=["POST"])
def register_user():
    # get the data from the body of the request
    body_data = request.get_json()
    # create an instance of the User model
    user = User(
        name=body_data.get("name"),
        email=body_data.get("email")
    )

    # extract the password from the body
    password = body_data.get("password")

    # hash the password
    if password:
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")

    # add and commit to the db
    db.session.add(user)
    db.session.commit()

    # respond back
    return user_schema.dump(user), 201



