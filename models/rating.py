
from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

VALID_RATINGS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

class Rating(db.Model):
    __tablename__ = "rating"

    # structure of table
    rating_id = db.Column(db.Integer, primary_key=True)
    rating_date = db.Column(db.Date) 
    user_rating = db.Column(db.Integer)

    # F Keys linking to Book/User tables
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    user = db.relationship('User', back_populates='rating')
    book = db.relationship('Book', back_populates='rating')

class RatingSchema(ma.Schema):
    title = fields.String(required=True, validate=And(
        Length(min=2, error="Title must be at least 2 characters long"),
        Regexp('^[a-zA-Z0-9 ]+$', error="Title can only have alphanumeric characters")
    ))

    user_rating = fields.Integer(validate=OneOf(VALID_RATINGS))

    user = fields.Nested('UserSchema', only = ['name', 'email'])

    book = fields.List(fields.Nested('BookSchema', exclude=['rating']))

    class Meta:
        fields = ('rating_id', 'rating_date', 'user_rating', 'user', 'books')
        ordered = True

# Schema for handling one user/many users
rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)
