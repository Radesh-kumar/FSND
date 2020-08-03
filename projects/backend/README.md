# Full Stack Trivia API Backend

## Setting up

#### Download Python 3.7
#### Setup Virtual Enviornment (Virtualenv or pipenv)
#### PIP Dependencies

```bash
pip install -r requirements.txt
(or)
pipenv install -r requirements.txt  
```
##### Key Dependencies
#### Flask
#### SQLAlchemy
#### Flask-Cors


## Database Setup
### Please change database path in models.py(7th line ), test_flaskr.py(18th line)
Navigate to /backend
```bash
sudo -u postgres psql trivia < 'trivia.psql'
```

## Running the server

After Creating virtual environment Navigate /backend and
To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
 
## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

 

## Endpoints
#### GET '/categories'
Return all categories
#### GET '/categories/<int:id>/questions'
Return questions based on category
#### GET '/questions'
Returning Question with pagination=10 
#### POST '/questions/add'
Adding new question 
### DELETE '/questions/<int:question_id>'
Deleting a question using id 
#### POST '/questions/search'
Searching Questions 
#### POST '/play'
Return questions for playing quiz



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```