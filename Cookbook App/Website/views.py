#This file is for pages that users can access
from dataclasses import field
from click import pass_context
from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for
from . import db    #allows use of database
from flask_login import login_required, current_user   #flask plugins that let you easily track logged user
from .models import Recipe, User #import classes from models file
import json
from .classes import RecipeForm, SearchForm
from sqlalchemy import false, or_
from werkzeug.security import generate_password_hash, check_password_hash #password scrambler

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    recipeData = db.session.query(Recipe).\
        order_by(Recipe.date.desc())
    return render_template("home.html", user=current_user, recipes=recipeData)  #home page using logged in user

@views.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    post_searched = form.searched.data

    recipeData = db.session.query(Recipe).\
        order_by(Recipe.date.desc()).\
        filter(or_(Recipe.recipeIngredients.contains(post_searched), Recipe.recipeBody.contains(post_searched), 
            Recipe.recipeTags.contains(post_searched), Recipe.recipeName.contains(post_searched)))
    return render_template("search.html", user=current_user, recipes=recipeData)

@views.route('/add_new_recipe', methods=['GET', 'POST'])
@login_required
def add_new_recipe():
    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name')
        recipe_ingredients = request.form.get('recipe_ingredients')
        recipe_body = request.form.get('recipe_body')
        recipe_tags = request.form.get('recipe_tags')

        if len(recipe_name or recipe_ingredients or recipe_body) < 1:
            flash('Note field is empty', category='error')
        else:
            new_recipe = Recipe(recipeName=recipe_name, recipeIngredients=recipe_ingredients, recipeBody=recipe_body, 
                recipeTags=recipe_tags, user_id=current_user.id, recipeAuthor=current_user.firstName)
            db.session.add(new_recipe)
            db.session.commit()
            flash('Recipe added', category='success')

    return render_template("add_new_recipe.html", user=current_user)  #new recipe page using logged in user

@views.route('/my_recipes', methods=['GET', 'POST'])
@login_required
def my_recipes():
    recipeData = db.session.query(Recipe).\
        order_by(Recipe.date.desc())
    return render_template("my_recipes.html", user=current_user, recipes=recipeData)  #my recipes page using logged in user

@views.route('/my_recipes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    recipeData = db.session.query(Recipe).\
        filter((Recipe.id.contains(id)))
    if request.method == 'POST':
        if request.form.get('submit') == 'submit':
            recipe_name = request.form.get('recipe_name')
            recipe_ingredients = request.form.get('recipe_ingredients')
            recipe_body = request.form.get('recipe_body')
            recipe_tags = request.form.get('recipe_tags')
            if len(recipe_name or recipe_ingredients or recipe_body) < 1:
                flash('Note field is empty', category='error')
            else:
                currentRecipe = Recipe.query.get(id)
                currentRecipe.recipeName = recipe_name
                currentRecipe.recipeIngredients = recipe_ingredients
                currentRecipe.recipeBody = recipe_body
                currentRecipe.recipeTags = recipe_tags
                db.session.commit()
                flash('Recipe updated', category='success')
    return render_template('edit_recipe.html', user=current_user, recipes=recipeData)

@views.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        passwordNew = request.form.get('passwordNew')
        passwordCurrent = request.form.get('passwordCurrent')
        fieldChanged = False

        userEmails = User.query.filter_by(email=email).first() #search database for users with the entered email and give the first result
        if check_password_hash(current_user.password, passwordCurrent):
            if email != current_user.email:    #determine if email already in use by another account
                if userEmails:
                    flash('Email already exists', category='error')
                elif len(email) < 4: #if email is shorter than 4 characters
                    flash('Email must be greater than 4 characters', category='error')
                else:
                    current_user.email = email
                    fieldChanged = True
            if first_name != current_user.firstName:
                if not first_name:
                    flash('Name cannot be empty', category='error')
                else:
                    current_user.firstName = first_name
                    fieldChanged = True
            if passwordNew:
                if len(passwordNew) < 7:
                    flash('Pass must be at least 7 characters', category='error')
                elif passwordNew == passwordCurrent:
                    flash('Passwords must be different', category='error')
                else:
                    current_user.password = generate_password_hash(passwordNew, method='sha256') #hashes password
                    fieldChanged = True
            else:
                flash('Account updated!', category='success')   #No changes were made, but password was put in correct
                return redirect(url_for('views.user_profile'))
        else:
                flash('Incorrect password', category='error')
        if fieldChanged == True:
            db.session.commit()     #at least 1 field got altered after correct current password, commit changes
            flash('Account updated!', category='success')
            return redirect(url_for('views.user_profile')) #reloads page after update
        return render_template('user_profile.html', user=current_user)
    else:
        return render_template('user_profile.html', user=current_user)

@views.route('/delete-recipe', methods=['POST'])
def delete_recipe():
    recipe = json.loads(request.data)
    recipeId = recipe['recipeId']
    recipe = Recipe.query.get(recipeId)
    if recipe:
        if recipe.user_id == current_user.id:
            db.session.delete(recipe)
            db.session.commit()
            flash('Recipe deleted', category='success')
    return jsonify({})  #turn into a returnable json object because returning something is a requirement