
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.book import Book
from models.wishlist import Wishlist, wishlist_schema

wishlists_bp = Blueprint('wishlists', __name__, url_prefix="/<int:book_id>/wishlists")
    
@wishlists_bp.route("/", methods=["POST"])
@jwt_required()
def create_wishlist(book_id):
    body_data = request.get_json()
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    if book:
        wishlist = Wishlist(
            wishlist_title = body_data.get('message'),
            user_id = get_jwt_identity(),
            book = book
        )
        db.session.add(wishlist)
        db.session.commit()
        return wishlist_schema.dump(wishlist), 201
    else:
        return {"error": f"Book with id {book_id} doesn't exist"}, 404
    
@wishlists_bp.route("/<int:wishlist_id>", methods=["DELETE"])
@jwt_required()
def delete_wishlist(book_id, wishlist_id):
    stmt = db.select(Wishlist).filter_by(id=wishlist_id)
    wishlist = db.session.scalar(stmt)
    if wishlist and wishlist.book.id == book_id:
        db.session.delete(wishlist)
        db.session.commit()
        return {"message": f"Wishlist with id {wishlist_id} has been deleted"}
    else:
        return {"error": f"Wishlist with id {wishlist_id} not found in book with id {wishlist_id}"}, 404
    
@wishlists_bp.route("/<int:wishlist_id>", methods=["PUT", "PATCH"])
@jwt_required()
def edit_wishlist(book_id, wishlist_id):
    body_data = request.get_json()
    stmt = db.select(Wishlist).filter_by(id=wishlist_id, book_id=book_id)
    book = db.session.scalar(stmt)
    if book:
        book.title = body_data.get('title') or book.title
        db.session.commit()
        return wishlist_schema.dump(wishlist)
    else:
        return {"error": f"Wishlist with id {wishlist_id} not found in book with id {book_id}"}
