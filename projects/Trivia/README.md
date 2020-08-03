# The Trivia API Documentation

The Trivia API is a full-stack application that allows users to play a trivia game wthere they can search for questions to answer, post new questions as well as delete questions. The aplications backend is built in Python, JS, React and a Postgres database where the data is stored, retrieved, edited and deleted by the application.

## Getting Started

### Understanding the project's structure

```
├── README.md
├── backend
│   ├── README.md
│   ├── __pycache__
│   ├── flaskr
│   ├── models.py
│   ├── pip
│   ├── requirements.txt
│   ├── test_flaskr.py
│   └── trivia.psql
├── env
│   ├── bin
│   ├── include
│   ├── lib
│   └── pyvenv.cfg
└── frontend
    ├── README.md
    ├── build
    ├── node_modules
    ├── package-lock.json
    ├── package.json
    ├── public
    └── src
````

# API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
## Running the server
From within the `backend` directory first ensure you are working using your created virtual environment.
To run the server, execute:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

# API Frontend

## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies: Node and NPM
This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:
```bash
npm install
```
>_tip_: **npm i** is shorthand for **npm install**
Open a terminal in `/frontend` directory and run:
```bash
npm install
```
and then run:
```bash
npm start
```
Open http://localhost:3000 to view the frontend in the browser.

#### Running tests
To set up tests, navigate to the `/backend` directory and run:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
```
next, change the self.database_path in test_flaskr.py (line 18) to match your PostgreSQL user and password.  
Then you can run tests by running from the `/backend` directory:
```bash
python test_flaskr.py
``

