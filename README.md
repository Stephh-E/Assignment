# Set Up
# To run, create a postgresql database using code:
CREATE DATABASE booky_db;

# Create a new user and give permissions with postgresql:
CREATE ROLE booky_dev GRANT ALL ON booky_db TO booky_dev;

# Edit .env to SQL DATABASE_URI
DATABASE_URI=”postgresql+psycopg2://booky_dev123456@localhost:5432/booky_db
JWT_SECRET_KEY=”secret”

# Start and activate VENV
python3 -m venv venv source .venv/bin/activate

# Install requirements 
pip3 install -r requirements.txt

# Create and seed tables
python3 -m flask db drop python3 -m flask db create python3 -m flask db seed

# Run Flask app
python3 -m flask run

# Explain the problem that this app will solve, and explain how this app solves or addresses the problem.
The Booky app assists book enthusiasts in managing and organising their reading preferences, books they intend to read, and books they have enjoyed. Many readers find it hard  to keep track of books they've liked, wishlists of books they’re interested in and their personal reviews and ratings.

Booky provides a solution by acting as a centralised platform where users can create and maintain curated wishlists of books they’d like to read, rate and review books they've read, and document their reading and connect with other readers.
Booky acts like a social media network for book lovers, helping users stay organised and allowing them to exchange recommendations. The app aims to enhance the reading experience and make it more interactive.

# Describe the way tasks are allocated and tracked in your project.
To manage tasks efficiently, I used Trello as my main tool for tracking progress and task completion. Categorised by stages such as 'To Do', 'In Progress', 'Completed' and ‘Review’. This visual organisation helped me track the status of each task effectively and reduce the chance of forgetting anything.

Some examples of cards I used are:

Research ORM Options
* revise SQLAlchemy and psql
* Setup Project Environment
* Initialize project repository.
* Configure venv
* Install necessary libraries in main.py.
* Design API Endpoints
* Create a list of required endpoints.
* Define request and response formats.
* Implement rating logic and validation.
* Setup User Authentication
* Implement user registration and login endpoints.
* Ensure secure password handling.

Version Control: I utilised Github for version control to keep a thorough record of changes to the code.I aimed to make the commit messages clear and descriptive to accurately track changes made. 
Reviewing/Testing: During reviewing and testing I found a lot of my errors were due to typos. I found PSQL hard to grasp and would have delved deeper into the app functions if I had more time/done more research of PSQL concept.

# List and explain the third-party services, packages and dependencies used in this app.

SQLAlchemy
An ORM library for Python
Provides tools intended to simplify database interactions 
In the Booky app, SQLAlchemy is used to manage relationships between models, change data records and perform CRUD operations

Flask
A WSGI web app framework. Provides a framework and libraries to build a web app.
Contains extensions, some used in Booky include Validation, bycrpyt, and JWT_extension

PostgreSQL
An open source object relational database(ORD) system
Used to store the database for the app

Psycopg2
A PostgreSQL database adapter
In Booky, Psycopg2 connects the postgreSQL db and executed SQL queries

Marshmallow
An ORM framework and library
In Booky Marshmallow is used to load schemas, serialise data into JSON format, handle nested relationships and validate input

JWT Extended
A flask extension supporting JSON Web tokens
Used in Booky to create web access tokens so that a user is identified and authorised in order to secure routes

Bcrypt
Used to hash passwords, Bcrypt is used in the app to ensure safe storage of passwords so they are hidden from unauthorised viewing

ThunderClient 
An API client extension used in VS code to check if the requests work
Used it in my app development as I liked it’s easy integration as opposed to Postman or Insomnia which exist in a different environment

# Explain the benefits and drawbacks of this app’s underlying database system.
I chose PostgresQL due to:

* It’s extensibility, that I could create my own functions as needed
* Has adjustable parameters, whereas other software is less adaptable
* It is ACID compliant, and supports high concurrent loads. PostgreSQL error functions are very useful. Changes made to tables can be seen immediately. 
* Postgres security is strong and has good recognition in the industry.

Drawbacks:

* Psql is criticised as being slower than MYSQL, so if the project was larger this may be an issue
* Large learning curve - I found learning PSQL to be quite difficult

# Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.

Object relational mapping (ORM) connects relational databases to object oriented programs(OOP).The ORM used in Booky is SQLALchemy. The purpose of an ORM is to simplify interactions with the database. Developers interact with the database through objects and methods rather than in just SQL queries. 

As well as making the development process simpler, SQLALchemy is used in this app to seed data for the app, and to generate and manage schemas.

Interactions you can perform are under the CRUD acronym, creating, reading, updating and deleting.

# Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design. 

![alt text](<images/Book rec_ ERD.png>)

I ended up changing the ERD I orignally made, in order to simplify the process. Instead of using an 'Interactions' table I opted for a 'Ratings' tables for rating the books a user has read.

Updated Entity Relationships:

USER MODEL

Attributes
* user_id = Int & Primary Key
* name = Str
* email = Str, not null
* password = Str, not null
* is_admin = Boolean, default is false

One-to-Many with Rating: A user can have multiple ratings 

One-to-One with Wishlist: A user can have one wishlist

RATING MODEL

Attributes
* rating_id = Int & Primary Key
* book_id = Int, Foreign Key & not null
* user_id = Int, Foreign Key & not null
* user_rating = Integer

Associations
Many-to-One with User: Multiple ratings per single user 

Many-to-One with Movie: Multiple ratings can exist for each book.

Wishlist Model

Attributes
* wishlist_id = Int & Primary Key
* watchlist_title = String, 20 character limit
* book_id = Int, Foreign Key & not null
* user_id = Int, Foreign Key & not null

Associations
Many-to-Many with BOok: Many wishlists can exist with multiple books

One-to-One with User: One wishlist can exist to one user.

Book Model

Attributes
* book_id = Int & primary_key
* title = Str, character limit 60
* description = Text
* genre = Str

Associations
Many-to-Many with Wishlist: Many books can exist within multiple wishlists.

One-to-Many with Rating: A book can have many ratings.

# Explain the implemented models and their relationships, including how the relationships aid the database implementation.

The models used in the app are book, rating, user, and wishlist.

# Book Model (book.py)
* The Book Model table has columns for id, book_title, description and genre.
* The rating relationship establishes a one-to-many relationship with the Rating model. Each book can have multiple ratings. The back_populates='book' -  is used to define the reverse relationship in the Rating model
* The wishlist relationship establishes a one-to-many relationship with the Wishlist model. Each book can be in multiple wishlists. The back_populates='book' option is used to define the reverse relationship in the Wishlist model

* Schema
* BookSchema is used to serialise and deserialise Book objects. It includes fields for book_title, genre, rating, and wishlist
* Rating is a nested field that includes only user_rating from the * RatingSchema
* Wishlist is a list of nested WishlistSchema objects, excluding the book field


# Rating Model (rating.py)
Defines the rating table with columns for id, user_id, book_id, and user_rating
User Relationship establishes a many-to-one relationship with the User model. Each rating is associated with a single user. The back_populates='ratings' option is used to define the reverse relationship in the User model
Book Relationship establishes a many-to-one relationship with the Book model. Each rating is associated with one book. The back_populates='rating' option is used to define the reverse relationship in the Book model
User Model (user.py)
Defines the user table with columns for id, username, email, and password.
Ratings Relationship establishes a one-to-many relationship with the Rating model. A user can have multiple ratings. 
back_populates='user' option is used to define the reverse relationship in the Rating model.
Wishlist Relationship establishes a one-to-many relationship with the Wishlist model. A user can have multiple wishlist entries. The back_populates='user' option is used to define the reverse relationship in the Wishlist model.
Wishlist Model (wishlist.py)
Defines the wishlist table with columns for id, user_id, and book_id
User Relationship establishes a many-to-one relationship with the User model. Each wishlist entry is associated with one user. The back_populates='wishlist' option is used to define the reverse relationship in the User model.
Book Relationship establishes a many-to-one relationship with the Book model. Each wishlist entry is associated with one book. The back_populates='wishlist' option is used to define the reverse relationship in the Book model.


The relationships aid the database implementation through:
Ensuring data integrity e.g. deleting all associated ratings and wishlist entries when a book is deleted
Ensuring data aggregation, e.g. you can aggregate ratings for a book or list all books in a user's wishlist without having to write complex SQL
In grouping related entities together, these relationships help in logical structuring the database schema, making it easier to understand.

# Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:
* HTTP verb
* Path or route
* Any required body or header data
* Response

POST /auth/register
Registers a new user
Required body data should be in JSON format and must include: name(string), email(string), password(string)
Email must be unique and email and password must not be null
An example of this is { "name": "Buffy Summers", "email": "buffysummers@example.com", "password": "ilovespike" }
The response will include details of the created user, as defined by the user_schema. This endpoint returns the name and an id, leaving out the hashed password. 
Example response: { "name": "Buffy Summers", "email": "buffysummers@example.com, "id": 1 }

POST /auth/login
Allows a registered user to login
Required body data should be in JSON format and must include: email(string), password(string), auth token(string), is_admin(boolean)
An example is  {"email": "buffysummers@example.com", "password": "ilovespike" }
If successful, the request response shows the JWT token created, the users name and their admin status
If unsuccessful Error 401 is returned

POST /books
Creates a new book
Required body data should be in JSON format and must include: book_title(string), decription(string), genre(string)

POST /rating
Creates a new rating
Required body data should be in JSON format and must include: book_id(Integer), user_id(Integer), user_rating(Integer)(must be between 1-10)

POST /wishlist
Creates a new wishlist
Required body data should be in JSON format and must include: wishlist_title(String), user_id(Integer), book(String)
If book exists - data is retrieved from book table, else Error 404 is returned 

GET /books
Retrieves all books from book table
If successful a list of all books is returned
If unsuccessful error message is displayed

GET /books/4
Retrieves select book from book table from the book_id
Required body data should be in JSON format and must include: book_id(Integer), book(String)
If successful retrieve book with corresponding book_id, if unsuccessful Error 404 is returned

GET /rating
Retrieves all ratings from rating table 
Checks for ratings in rating table, if successful a list of all books, if unsuccessful Error 404 is returned

GET /rating/4
Retrieves all ratings from rating table 
Rating_id(Integer)(id of book rating to retrieve)
If successful, book with the corresponding id is retrieved, if unsuccessful Error 404 message is returned 

DELETE /books/6
Deletes book with corresponding book_id
Check if user is an admin, check if book exists
If book exists, book is deleted, if book doesn't exist Error 404 is returned
If they aren’t an admin of the wishlist Error 403 is returned

DELETE /rating/6
Deletes rating with the corresponding rating_id
Check if user is admin, if they’re admin, check rating exists, if rating exists then rating is deleted, if rating does not exist then return error 404 not found, if they’re not an admin Error 403 is returned

DELETE /wishlist/6
Deletes wishlist with the corresponding wishlist_id
Check if user is admin, if they’re admin, check wishlist exists, if wishlist exists then wishlist is deleted, if rating does not exist then return error 

PUT PATCH /books/5
Changes data in book table
Update data from the body of the request, get the book from the db where the field needs to be updated
If book exists, check user if user is admin, update the fields, if book doesn’t exist return error 403

PUT PATCH /rating/5
Modifies data in rating table
Updates data from the body of the request and get the rating from the db with fields to be updated
Is rating exists, check user, if user is admin update the fields, if rating doesn’t exist or user isn’t admin Error is returned

PUT PATCH /wishlist/5
Modifies data in wishlist table
Update data from the body of the request, get the rating from the db with fields to be updated
Is wishlist exists, check user, if user is admin update the fields, if wishlist doesn’t exist or user isn’t admin Error is returned
