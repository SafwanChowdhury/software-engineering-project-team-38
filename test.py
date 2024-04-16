from datetime import datetime, timedelta
import os
import unittest
from flask import request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models

class CorrectUser():
    def __init__(self, username="Tester", email="test1@gmail.com", age=20, password_1="Testtest1", password_2="Testtest1", follow_redirects=True):
        self.username = username
        self.email = email
        self.age = age
        self.password_1 = password_1
        self.password_2 = password_2
        self.follow_redirects = follow_redirects

    def getData(self):
        data = dict(username=self.username, email=self.email, age=self.age, password_1=self.password_1, password_2=self.password_2, follow_redirects=self.follow_redirects)
        return data

class CorrectPayment():
    def __init__(self, country=None, name="Jane Doe", card_number="123456789101112", cvv=230, expiry_date=(datetime.now() + timedelta(weeks=1)).strftime("%m/%Y"), address_line_1="Flat 3 Birch House", city="London", postcode="HA39TE", follow_redirects=True):
        self.name = name
        self.card_number = card_number
        self.cvv = cvv
        self.expiry_date = expiry_date
        self.address_line_1 = address_line_1
        self.city = city
        self.postcode = postcode
        self.country = country
        self.follow_redirects = follow_redirects

    def getData(self):
        data = dict(
        name = self.name,
        card_number = self.card_number,
        cvv = self.cvv,
        expiry_date =self. expiry_date,
        address_line_1 = self.address_line_1,
        city = self.city,
        postcode = self.postcode,
        country = self.country,
        follow_redirects = self.follow_redirects)
        return data
    

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        
        for i in range(0,4):
            for j in range(1,6):
                user_obj = models.Scooter(in_use=False, LocationID=j)
                db.session.add(user_obj)
        db.session.commit()
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()

  

    # Should allow valid user to register i.e. redirects to correct page and user gets added to db
    def test_register_user_correct_1(self):
        tester = app.test_client(self)
        user = CorrectUser()
        response = tester.post('/register', data = user.getData())
        user_obj = models.User.query.filter_by(email=user.email).first()
        self.assertTrue(user_obj) # checks user is in database
        self.assertIn(b"Active Orders", response.data) # checks user has been redirected to dashboard


    # Should allow valid user to register i.e. redirects to correct page and user gets added to db
    def test_register_user_correct_2(self):
        tester = app.test_client(self)
        user = CorrectUser(username="New_Tester", email="valid-email@valid.com", age=18, password_1="ValidPassword9*", password_2="ValidPassword9*", follow_redirects=True)
        response = tester.post('/register', data = user.getData())
        user_obj = models.User.query.filter_by(email=user.email).first()
        self.assertTrue(user_obj) # checks user is in database
        self.assertIn(b"Active Orders", response.data) # checks user has been redirected to dashboard

    def test_login_user_correct_1(self):
        tester = app.test_client(self)
        user = CorrectUser()
        tester.post('/register', data=user.getData()) # registers new valid user using same code from above test
        response = tester.post('/login', data = dict(email=user.email, password=user.password_1), follow_redirects=True) # attempts to log in user which has been registered correctly
        self.assertIn(b"Active Orders", response.data)

    def test_login_user_correct_2(self):
        tester = app.test_client(self)
        user = CorrectUser(username="New_Tester", email="valid-email@valid.com", age=18, password_1="ValidPassword9*", password_2="ValidPassword9*", follow_redirects=True)
        tester.post('/register', data=user.getData()) # registers new valid user using same code from above test
        response = tester.post('/login', data = dict(email=user.email, password=user.password_1), follow_redirects=True) # attempts to log in user which has been registered correctly
        self.assertIn(b"Active Orders", response.data)

    # Tests if a logged in user is correctly logged out in the session 
    def test_logout(self):
        with app.test_client(self) as c:
            user = CorrectUser()
            c.post('/register', data = user.getData())
            self.assertIn("email", session)
            c.post("/logout")
            self.assertNotIn("email", session)
    
    # Should not allow two users with the same email address
    def test_register_user_incorrect_1(self):
        with app.test_client(self) as c:
            same_email = "validEmail@test.com"
            user1 = CorrectUser(email=same_email)
            user2 = CorrectUser(username=user1.username+"change", email=same_email, age=user1.age+3, password_1=user1.password_1+"change", password_2=user1.password_1+"change", follow_redirects=True)
            c.post('/register', data = user1.getData())
            c.post("/logout")
            c.post('/register', data = user2.getData())
            user_count = models.User.query.filter_by(email=same_email).count()
            user2_obj = models.User.query.filter_by(username=user1.username+"change").first()
            self.assertEqual(user_count, 1)
            self.assertFalse(user2_obj)


    # # Should not allow to register user with invalid email address - no "."
    def test_register_user_incorrect_2(self):
        tester = app.test_client(self)
        user = CorrectUser(email="emailwithnodot@failcom")
        response = tester.post('/register', data = user.getData())
        user_obj = models.User.query.filter_by(email=user.email).first()
        self.assertFalse(user_obj)
        self.assertIn(b'Enter your phone number', response.data)

    # # Should not allow invalid email address - no "@"
    def test_register_user_incorrect_3(self):
        tester = app.test_client(self)
        user = CorrectUser(email="emailwithnodotfail.com")
        response = tester.post('/register', data = user.getData())
        user_obj = models.User.query.filter_by(email=user.email).first()
        self.assertFalse(user_obj)
        self.assertIn(b'Enter your phone number', response.data)

    # Should not allow password with less than 8 characters
    def test_register_user_incorrect_4(self):
        tester = app.test_client(self)
        user = CorrectUser(password_1="Length1", password_2="Length1")
        response = tester.post('/register', data = user.getData())
        user_obj = models.User.query.filter_by(email=user.email).first()
        self.assertFalse(user_obj)
        self.assertIn(b'Enter your phone number', response.data)

    # # Should not allow password with no numerical digit
    def test_register_user_incorrect_5(self):
        tester = app.test_client(self)
        user = CorrectUser(password_1="Nonumericaldigit", password_2="Nonumericaldigit")
        response = tester.post('/register', data = user.getData())
        user_obj = models.User.query.filter_by(email=user.email).first()
        self.assertFalse(user_obj)
        self.assertIn(b'Enter your phone number', response.data)

    # Should not allow password with no capital letter
    def test_register_user_incorrect_6(self):
        tester = app.test_client(self)
        user = CorrectUser(password_1="nocapitalletter1", password_2="nocapitalletter1")
        response = tester.post('/register', data = user.getData())
        user_obj = models.User.query.filter_by(email=user.email).first()
        self.assertFalse(user_obj)
        self.assertIn(b'Enter your phone number', response.data)

    # Should not allow unmatching passwords
    def test_register_user_incorrect_7(self):
        tester = app.test_client(self)
        user = CorrectUser(password_1="Password1*", password_2="Password2*")
        response = tester.post('/register', data = user.getData())
        user_obj = models.User.query.filter_by(email=user.email).first()
        self.assertFalse(user_obj)
        self.assertIn(b'Enter your phone number', response.data)

    
    # Should not allow user with null username to register
    def test_register_user_incorrect_8(self):
        tester = app.test_client(self)
        user = CorrectUser(username="")
        response = tester.post('/register', data = user.getData())
        user_obj = models.User.query.filter_by(email=user.email).first()
        self.assertFalse(user_obj)
        self.assertIn(b'Enter your phone number', response.data)

    # def test_booking_scooter_correct_1(self):
    #     # with app.test_client(self) as c:
 
    #     #     response = c.post('/', data = dict(location="1", hours="1", follow_redirects = True))
    #     #     self.assertTrue(response.status)
    #     with app.test_client() as c:
    #         c.post("/add_pricing")
    #         user = CorrectUser()
    #         c.post('/register', data = user.getData())
    #         payment = CorrectPayment()                
    #         # response = c.post("/payment?location=2&hours=1", data = payment.getData())
    #         self.assertIn(response.data, b"Active Orders")


if __name__ == '__main__':
    unittest.main()

