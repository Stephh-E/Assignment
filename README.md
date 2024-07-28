# # Set Up
# To run, create a postgresql database using code:
CREATE DATABASE booky_db;

Create a new user and give permissions with postgresql:
CREATE ROLE booky_dev GRANT ALL ON booky_db TO booky_dev;

Edit .env to SQL DATABASE_URI
DATABASE_URI=”postgresql+psycopg2://booky_dev123456@localhost:5432/booky_db
JWT_SECRET_KEY=”secret”

Start and activate VENV
python3 -m venv venv source .venv/bin/activate

Install requirements 
pip3 install -r requirements.txt

Create and seed tables
python3 -m flask db drop python3 -m flask db create python3 -m flask db seed

Run Flask app
python3 -m flask run
