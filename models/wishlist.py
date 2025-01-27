from init import db, ma
from marshmallow import fields 

class Wishlist(db.Model):
    __tablename__ = "wishlist"

    # structure of table
    id = db.Column(db.Integer, primary_key=True)
    wishlist_title = db.Column(db.String(20), nullable=False)

    # F Key link to Book/User tables
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    user = db.relationship('User', back_populates='wishlist')
    book = db.relationship('Book', back_populates='wishlist')

    # {
    #   id: 1,
    #   title: "Wishlist 1"
    #   description: "Wishlist 1 desc",
    #   date
    #}

    class WishlistSchema(ma.Schema):
        user = fields.Nested('UserSchema', only=[ "id", "name", "email"])

        book = fields.Nested('BookSchema', exclude=['wishlist'])


        class Meta:
            fields = ("id", "wishlist_title", "book", "user")
    
    wishlist_schema = WishlistSchema()
    wishlists_schema = WishlistSchema(many=True)