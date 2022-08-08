function deleteRecipe(recipeId){    //calls /delete-recipe in views.py, javascript command to delete a line
    fetch('/delete-recipe', {
        method: 'POST',
        body: JSON.stringify({recipeId: recipeId})  //turn recipeid into a string to pass it on
    }).then((_res) => {
        window.location.href = ""; //redirect 
    })
}

function editRecipe(recipeId){    //calls /edit-recipe in views.py, javascript command to pass recipe to edit page
    fetch('/recipeEdit', {
        method: 'POST',
        body: JSON.stringify({recipeId: recipeId})  //turn recipeid into a string to pass it on
    }).then((_res) => {
        window.location.href = "views.my_recipes"; //redirect
    })
}

function favoriteRecipe(recipeId){    //calls /favorite-recipe in views.py
    fetch('/recipeFavorite', {
        method: 'POST',
        body: JSON.stringify({recipeId: recipeId})  //turn recipeid into a string to pass it on
    }).then((_res) => {
        window.location.href = ""; //redirect
    })
}

function unfavoriteRecipe(recipeId){    //calls /unfavorite-recipe in views.py
    fetch('/unrecipeFavorite', {
        method: 'POST',
        body: JSON.stringify({recipeId: recipeId})  //turn recipeid into a string to pass it on
    }).then((_res) => {
        window.location.href = ""; //redirect
    })
}