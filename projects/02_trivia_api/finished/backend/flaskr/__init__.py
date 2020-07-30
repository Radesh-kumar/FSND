import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

from utils import get_paginated_questions

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={'/': {'origins': '*'}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        """ Set Access Control """

        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    @app.route('/categories')
    def get_all_categories():
        '''
        Handles GET requests for getting all categories.
        '''
        try:
            categories = Category.query.all()

            # Format categories to match front-end
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type

            # return successful response
            return jsonify({
                'success': True,
                'categories': categories_dict
            }), 200
        except Exception:
            abort(500)

    @app.route('/questions')
     def get_questions():
        """
        Get all questions, categories and total questions from database
        :return: Questions, categories and total questions
        """
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        questions = [question.format() for question in Question.query.all()]
        page = int(request.args.get('page', '0'))
        upper_limit = page * 10
        lower_limit = upper_limit - 10
        return jsonify({
            'questions': questions[
                         lower_limit:upper_limit] if page else questions,
            'total_questions': len(questions),
            'categories': categories
        })

    @app.route('/questions/<int:id>', methods=['DELETE'])
        def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def post_question():
        '''
        Handles POST requests for creating new questions and searching questions.
        '''
        # load the request body
        body = request.get_json()

        # if search term is present
        if (body.get('searchTerm')):
            search_term = body.get('searchTerm')

            # query the database using search term
            selection = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            # 404 if no results found
            if (len(selection) == 0):
                abort(404)

            # paginate the results
            paginated = paginate_questions(request, selection)

            # return results
            return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': len(Question.query.all())
            })
        # if no search term, create new question
        else:
            # load data from body
            new_question = body.get('question')
            new_answer = body.get('answer')
            new_difficulty = body.get('difficulty')
            new_category = body.get('category')

            # ensure all fields have data
            if ((new_question is None) or (new_answer is None)
                    or (new_difficulty is None) or (new_category is None)):
                abort(422)

            try:
                # create and insert new question
                question = Question(question=new_question, answer=new_answer,
                                    difficulty=new_difficulty, category=new_category)
                question.insert()

                # get all questions and paginate
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                # return data to view
                return jsonify({
                    'success': True,
                    'created': question.id,
                    'question_created': question.question,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })

            except:
                # abort unprocessable if exception
                abort(422)


    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """
        Search for questions using the search term
        :return: Searched questions and total questions
        """
        search_term = request.json.get('searchTerm', '')
        questions = [question.format() for question in Question.query.all() if
                     re.search(search_term, question.question, re.IGNORECASE)]
        return jsonify({
            'questions': questions,
            'total_questions': len(questions)
        })


    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        try:
            questions = Question.query.filter(
                Question.category == str(category_id)).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': category_id
            })
        except:
            abort(404)

    
    @app.route('/quizzes', methods=['POST'])
    def play_quiz_question():
         '''
        Handles POST requests for playing quiz.
        '''

        # load the request body
        body = request.get_json()

        # get the previous questions
        previous = body.get('previous_questions')

        # get the category
        category = body.get('quiz_category')

        # abort 400 if category or previous questions isn't found
        if ((category is None) or (previous is None)):
            abort(400)

        # load questions all questions if "ALL" is selected
        if (category['id'] == 0):
            questions = Question.query.all()
        # load questions for given category
        else:
            questions = Question.query.filter_by(category=category['id']).all()

        # get total number of questions
        total = len(questions)
        # defines a random question generator method
        def get_random_question():
            return questions[random.randint(0, len(questions)-1)]

        # get random question for the next question
        next_question = get_random_question()

        # defines boolean used to check that the question
        # is not a previous question
        found = True

        while found:
            if next_question.id in previous_questions:
                next_question = get_random_question()
            else:
                found = False

        return jsonify({
            'success': True,
            'question': next_question.format(),
        }), 200

    # Error handler for Bad request error (400)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request error'
        }), 400

    # Error handler for resource not found (404)
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    # Error handler for internal server error (500)
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'An error has occured, please try again'
        }), 500

    # Error handler for unprocesable entity (422)
    @app.errorhandler(422)
    def unprocesable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    return app
