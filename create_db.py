from init import app, db

#creates the database
with app.app_context():
    db.create_all()
    