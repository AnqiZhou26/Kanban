import json
import pytest
import unittest
import requests
from app import app, db, Todo, User
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

class TestApp(unittest.TestCase):

    # initiate a test object based on app
    def setUp(self):
        app.config['TESTING'] = True
        self.tester = app.test_client()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        # clear current db session
        db.session.remove()
        # drop all tables in db
        db.drop_all()

    # test whether entering correct login info can redirect to index.html
    # test whether Kanban board is displayed
    def test_login(self):
        response = self.tester.post("/signup", data={'username': 'testperson', 'password': 'passwrd'})
        rv = self.tester.post("/login", data={'username': 'testperson', 'password': 'passwrd'})
        page = self.tester.get("/", content_type='html/text', follow_redirects=True)
        data = page.get_data(as_text=True)
        self.assertEqual(response.status_code, 302)
        self.assertIn('Kanban board', data)

    # test whether the signup method successfully adds user to db
    def test_signup(self):
        response = self.tester.post("/signup", data={'username': 'testperson', 'password': 'passwrd'})
        user = User.query.filter_by(username='testperson').first()
        self.assertIsNotNone(user)

    # test incorrect login behaviors - should redirect to login page
    def test_name_password(self):
        # Case1: empty login input parameters
        response = self.tester.post("/login", data={'username': '', 'password': ''}, follow_redirects=True)
        resp = response.data
        self.assertIn(b"Please Sign In", resp)

        # Case2: partially empty login inputs
        rv = self.tester.post("/login", data={'username': 'testperson', 'password': ''}, follow_redirects=True)
        resp = response.data
        self.assertIn(b"Please Sign In", resp)

        # Case3: wrong password
        rv = self.tester.post("/login", data={'username': 'testperson', 'password': 'wrongpasswrd'}, follow_redirects=True)
        resp = response.data
        self.assertIn(b"Please Sign In", resp)

        # Case 4: wrong username
        rv = self.tester.post("/login", data={'username': 'wrongname', 'password': 'passwrd'},
                              follow_redirects=True)
        resp = response.data
        self.assertIn(b"Please Sign In", resp)

    def test_add(self):
        # after login
        response = self.tester.post("/signup", data={'username': 'testperson', 'password': 'passwrd'})
        rv = self.tester.post("/login", data={'username': 'testperson', 'password': 'passwrd'})

        # add one task
        response = self.tester.post(
            '/add',
            data={'todoitem': 'testitem1'},
        )
        # check if the added task appears on the dashboard
        rv = self.tester.get("/", content_type ='html/text', follow_redirects=True)
        self.assertIn('testitem1', rv.get_data(as_text=True))
        self.assertEqual(response.status_code, 302)

    def test_ongoing(self):
        # after login
        response = self.tester.post("/signup", data={'username': 'testperson', 'password': 'passwrd'})
        rv = self.tester.post("/login", data={'username': 'testperson', 'password': 'passwrd'})
        # add one task with status ongoing to the db & save
        testitem2 = Todo(text='testitem2', status='ongoing', removed=False)
        db.session.add_all([testitem2])
        db.session.commit()
        # whether it correctly displays on the dashboard
        ongoing_item = Todo.query.filter_by(text='testitem2').first()
        rv = self.tester.get("/", content_type='html/text', follow_redirects=True)
        self.assertIn('testitem2', rv.get_data(as_text=True))
        self.assertIsNotNone(ongoing_item)

    def test_complete(self):
        # after login
        response = self.tester.post("/signup", data={'username': 'testperson', 'password': 'passwrd'})
        rv = self.tester.post("/login", data={'username': 'testperson', 'password': 'passwrd'})
        # add one task with status complete to the db & save
        testitem3 = Todo(text='testitem3', status='complete', removed=False)
        db.session.add_all([testitem3])
        db.session.commit()
        complete_item = Todo.query.filter_by(text='testitem3').first()
        to_do_item = Todo.query.filter_by(status='incomplete').first()
        # check its display
        rv = self.tester.get("/", content_type='html/text', follow_redirects=True)
        self.assertIn('testitem3', rv.get_data(as_text=True))
        self.assertIsNotNone(complete_item)
        self.assertIsNone(to_do_item)

    def test_removed(self):
        # after login
        response = self.tester.post("/signup", data={'username': 'testperson', 'password': 'passwrd'})
        rv = self.tester.post("/login", data={'username': 'testperson', 'password': 'passwrd'})
        # add one task that has been removed
        testitem4 = Todo(text='testitem4', status='complete', removed=True)
        db.session.add_all([testitem4])
        db.session.commit()
        # it should not appear on the kanban
        remove_item = Todo.query.filter_by(removed=True).first()
        rv = self.tester.get("/", content_type='html/text', follow_redirects=True)
        self.assertNotIn('testitem4', rv.get_data(as_text=True))
        self.assertIsNotNone(remove_item)





if __name__ == '__main__':
    unittest.main()