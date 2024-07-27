import functools

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.book import Book, books_schema, book_schema
from models.rating import Rating
from models.user import User
from models.wishlist import Wishlist
from controllers.wishlist_controller import wishlists_bp
from controllers.rating_controller import rating_bp

books_bp = Blueprint('books', __name__, url_prefix='/books')
books_bp.register_blueprint(wishlists_bp)

def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        
        if user.is_admin:
            # if user is admin continue and run the decorated function
            return fn(*args, **kwargs)
    
        else:
            
            return {"error": "Not authorised to delete a book"}, 403
        
    return wrapper

# http://localhost:8080/books - GET
@books_bp.route('/')
def get_all_books():
    stmt = db.select(Book).order_by(Book.release.desc())
    books = db.session.scalars(stmt)
    return books_schema.dump(books)


# http://localhost:8080/books/4 - GET
@books_bp.route('/<int:book_id>')
def get_one_book(book_id): 
    stmt = db.select(Book).filter_by(id=book_id) # select * from books where id=4
    book = db.session.scalar(stmt)
    if book:
        return book_schema.dump(book)
    else:
        return {"error": f"Book with id {book_id} not found"}, 404
    

# http://localhost:8080/books - POST
@books_bp.route('/', methods=["POST"])
@jwt_required()
def create_book():
    body_data = book_schema.load(request.get_json())
    
    book = Book(
        title = body_data.get('title'),
        description = body_data.get('description'),
        genre = body_data.get('genre'),
        user_id = get_jwt_identity()
    )
    # Add that to session and commit

    db.session.add(book)
    db.session.commit()
    
    return book_schema.dump(book), 201

# https://localhost:8080/books/6 - DELETE
@books_bp.route('/<int:book_id>', methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_book(book_id):
    # # check user's admin status
    # is_admin = is_user_admin()
    # if not is_admin:
    #     return {"error": "Not authorised to delete a movie"}, 403
    # get the movie from the db with id = movie_id

    stmt = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(stmt)

    if book:
        # delete the book from the session and commit
        db.session.delete(book)
        db.session.commit()
        
        return {'message': f"Book'{book.title}' deleted successfully"}
    
    else:
        # return error msg
        return {'error': f"Book with id {book_id} not found"}, 404
    
# http://localhost:8080/books/5 - PUT, PATCH
@books_bp.route('/<int:book_id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_book(book_id):
    # Get the data updated from the body of the request
    body_data = book_schema.load(request.get_json(), partial=True)
    # get the book from the db that needs to be updated
    stmt = db.select(Book).filter_by(id=book_id)
    book = db.session.scalar(stmt)
    
    if book:
        if str(book.user_id) != get_jwt_identity():
            return {"error": "Only the admin can edit the book"}, 403
        
        book.title = body_data.get('title') or book.title
        book.description = body_data.get('description') or book.description
        book.genre = body_data.get('genre') or book.genre
    
        db.session.commit()
        return book_schema.dump(book)

    else:
      
        return {'error': f'Book with id {book_id} not found'}, 404
    

# This function has been replaced by the authorise_as_admin decorator
def is_user_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin