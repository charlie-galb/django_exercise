# TK Onboarding Recipe API

A CRUD API for storing and managing recipes.  

## Setup

Clone the repo: 
```
git@github.com:charlie-galb/django_exercise.git
```  
Move into the project directory: 
```
cd django_exercise
```
Start the docker image: 
```
docker-compose up
```

## Tests

To run the tests:
```  
docker-compose run --rm app sh -c "python manage.py test"
```

## Endpoints

**POST /api/recipe/recipes/**

Creates a new recipe. 

*Sample request*
```
{
    "name": "Thai green curry",
    "description": "Cook peppers and tofu in coconut milk and serve.",
    "ingredients": [
        {"name": "Peppers"},
        {"name": "Coconut milk"}
    ]
}
```
*Sample response*
```
{
    "id": 2,
    "name": "Thai green curry",
    "description": "Cook peppers and tofu in coconut milk and serve.",
    "ingredients": [
        {
            "name": "Coconut milk"
        },
        {
            "name": "Peppers"
        }
    ]
}
```
**Get /api/recipe/recipes**

Retrieves all recipes. 

*Sample response*
```
[
    {
        "id": 1,
        "name": "Chocolate cake",
        "description": "Put the bits in and bake.",
        "ingredients": [
            {
                "name": "Chocolate"
            },
            {
                "name": "Cake"
            }
        ]
    },
    {
        "id": 3,
        "name": "Thai green curry",
        "description": "Cook peppers and tofu in coconut milk and serve.",
        "ingredients": [
            {
                "name": "Peppers"
            },
            {
                "name": "Coconut milk"
            }
        ]
    }
]
```
**GET /api/recipe/recipes/:id**

Retrieves a single recipe. 

*Sample response*
```
{
    "id": 1,
    "name": "Chocolate cake",
    "description": "Put the bits in and bake.",
    "ingredients": [
        {
            "name": "Cake"
        },
        {
            "name": "Chocolate"
        }
    ]
}
```
**PATCH /api/recipe/recipes/2/**

Updates a recipe. 

*Sample request*
```
{
    "ingredients": [
        {"name": "Tofu"},
    ]
}
```
*Sample response*
```
{
    "id": 2,
    "name": "Thai green curry",
    "description": "Cook peppers and tofu in coconut milk and serve.",
    "ingredients": [
        {
            "name": "Tofu"
        }
    ]
}
```
**Delete /api/recipe/recipes/3/**

Deletes a single recipe. 

*Sample response*

** HTTP 204 (NO CONTENT) **
