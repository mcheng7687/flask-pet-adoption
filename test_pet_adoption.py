from app import app
from unittest import TestCase
from flask import Flask, render_template, flash, redirect, sessions, request
from models import db, Pet

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_adoption_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

class PetAdoptionTestCase(TestCase):
    """Test all functions in pet adoption app.py"""

    def setUp(self):
        """Clean up any pets in database and adds new pet"""
        db.drop_all()
        db.create_all()

        pet = Pet(id=1, name = "Fluffy", species = "cat", photo_url = "https://med.stanford.edu/news/all-news/2021/09/cat-fur-color-patterns/_jcr_content/main/image.img.620.high.jpg/cat_by-Kateryna-T-Unsplash.jpg", age = 2, notes = "Sleeps on faces", available = True)
        db.session.add(pet)
        db.session.commit()

    def tearDown(self):
        """Clean up any database transactions"""
        db.session.rollback()

    def test_homepage(self):
        """Test home page"""
        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('<h1>Melvin Pet Adoption Agency</h1>',html)
            self.assertIn('<p>Name: Fluffy</p>',html)
    
    def test_add_pet(self):
        """Test add pet form"""
        with app.test_client() as client:
            res = client.get("/add")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('<input id="name" name="name" required type="text" value="">',html)

    def test_add_pet_to_db(self):
        """Test add pet to database"""
        with app.test_client() as client:
            res = client.post("/add", data={'name':'Lucky','species':"dog","photo_url":"None", "age": "2", "notes":"Licks face"}, follow_redirects = True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('Lucky',html)

    def test_edit_form(self):
        """Test edit pet form"""
        with app.test_client() as client:
            res = client.get("/1")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('Sleeps on faces',html)

    def test_edit_pet_db(self):
        with app.test_client() as client:
            res = client.post("/1", data={"photo_url":"None", "notes":"Likes to sunbathe", "available":"False"}, follow_redirects = True)
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code,200)
            self.assertIn('Fluffy',html)