import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from utils import create_mock_question


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        """Tests question pagination success"""
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))


    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['questions'], list)
        self.assertLessEqual(len(data['questions']), 10)
        self.assertIsInstance(data['total_questions'], int)
        self.assertIsInstance(data['categories'], dict)

    def test_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_successfully_deleted(self):
        """Test for deleting a question.
        """
        mock_question_id = create_mock_question()
        response = self.client().delete(
            '/questions/{}'.format(mock_question_id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Question successfully deleted")

    def test_delete_same_question_twice(self):
        mock_question_id = create_mock_question()
        self.client().delete('/questions/{}'.format(mock_question_id))
        response = self.client().delete(
            '/questions/{}'.format(mock_question_id))
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_delete_questions_fail(self):
        res = self.client().delete('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_422_sent_deleting_non_existing_question(self):
        res = self.client().delete('/questions/afbdb')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
        """Tests question creation success"""
        questions_before = Question.query.all()
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        questions_after = Question.query.all()
        question = Question.query.filter_by(id=data['created']).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(questions_after) - len(questions_before) == 1)
        self.assertIsNotNone(question)

    def test_create_question_with_empty_data(self):
        """Test for ensuring data with empty fields are not processed."""
        request_data = {
            'question': '',
            'answer': '',
            'difficulty': 1,
            'category': 1,
        }
        response = self.client().post('/questions', json=request_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_search(self):
        request_data = {'searchTerm': 'what'}
        res = self.client().post('/search', data=json.dumps(request_data),
                                 content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['questions'], list)
        self.assertIsInstance(data['total_questions'], int)

    def test_empty_search(self):
        """Test for empty search term."""
        request_data = {
            'searchTerm': '',
        }
        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_get_questions_by_category(self):
        category_id = 1
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['questions'], list)
        self.assertIsInstance(data['total_questions'], int)
        self.assertEqual(data['current_category'], category_id)
        for question in data['questions']:
            self.assertEqual(question['category'], category_id)

    def test_400_if_questions_by_category_fails(self):
        """Tests getting questions by category failure 400"""
        response = self.client().get('/categories/100/questions')
        # load response data
        data = json.loads(response.data)
        # check response status code and message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_get_quiz_questions(self):
        request_data = {
            'previous_questions': [1, 2, 3, 4],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        res = self.client().post('/quizzes', data=json.dumps(request_data),
                                 content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        if data.get('question', None):
            self.assertNotIn(data['question']['id'], request_data['previous_questions'])

    def test_no_data_to_play_quiz(self):
        """Test for the case where no data is sent"""
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request error')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
