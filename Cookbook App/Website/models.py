from sqlalchemy import PrimaryKeyConstraint
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func     #makes it so you can import current date easily with func.now()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(30000))
    #date, using sqlalchemy.sql - func - func.now()
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #foreign key - associate entry with a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #classes are capitalized in python but sql with reference it as lower case

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    favorites = db.Column(db.String(50))    #used to store ID number of recipe that has been favorited
    #from entries
    recipes = db.relationship('Recipe')      #relays all the entries a user owns back to the user #this one needs to be capitalized

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipeName = db.Column(db.String(100))
    recipeIngredients = db.Column(db.String(10000))
    recipeBody = db.Column(db.String(30000))
    recipeTags = db.Column(db.String(10000))
    #author
    recipeAuthor = db.Column(db.String(150))
    #date, using sqlalchemy.sql - func - func.now()
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #foreign key - associate entry with a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))