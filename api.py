from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Nullable
from flask_restful import Resource, Api, reqparse, fields, marshal_with,abort 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app) 

#classes id, username, email, boards

#define UserModel class
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique= True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"User(name = {self.username}, email = {self.email})"

#Define request parser
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help = "Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help = "Email cannot be blank")

userFields = {
    'id':fields.Integer,
    'name':fields.String,
    'email':fields.String,
}

#Retrieves all users from database

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email = args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
    #201 means created

    
api.add_resource(Users, '/api/users/')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)
    
