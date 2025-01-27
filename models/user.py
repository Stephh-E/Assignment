from init import db, ma

class User(db.Model):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    wishlist = db.relationship('wishlist', back_populates="user")

class UserSchema(ma.Schema):
    class Meta:
        fields =("id", "name", "email","password", "is_admin")

# to handle a single user object
user_schema = UserSchema(exclude=["password"])

# to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])




