from . import db    #allows use of database
from flask_login import login_required, current_user   #flask plugins that let you easily track logged user
from .models import Recipe, User #import classes from models file
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import data_required, DataRequired

#create a search form
class SearchForm(FlaskForm):
    searched = StringField("searched", validators=[DataRequired()])
    submit = SubmitField("submit")

class RecipeForm(FlaskForm):
    title = StringField("recipe_name", validators=[DataRequired()])
    ingredients = StringField("recipe_ingredients", validators=[DataRequired()])
    body = StringField("recipe_body", validators=[DataRequired()])
    tags = StringField("recipe_tags")
    submit = SubmitField("submit")