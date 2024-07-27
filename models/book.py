from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

from init import db, ma

# Create genres
VALID_GENRE = ('Drama', 'Biography', 'Crime', 'Fantasy' 'Sci-fi', 'Romance', 'Comic', 'Self-help', 'Poetry', 'Classics')

class Book(db.Model):
    __tablename__ = "book"

    # structure of table
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)
    genre = db.Column(db.String)
    

    rating = db.relationship('Rating', back_populates='book', cascade='all, delete')
    wishlist = db.relationship('Wishlist', back_populates='book', cascade='all, delete')

class BookSchema(ma.Schema):

    book_title = fields.String(required=True, validate=And)

    genre = fields.String(validate=OneOf(VALID_GENRE))

    rating = fields.Nested('RatingSchema', only = ['user_rating'])

    watchlist = fields.List(fields.Nested('WishlistSchema', exclude=['book']))

    class Meta:
        fields = ('id', 'book_title', 'description', 'genre', 'rating', 'wishlist')
        ordered = True

# create schema for handling one/many users
book_schema = BookSchema()
books_schema = BookSchema(many=True)