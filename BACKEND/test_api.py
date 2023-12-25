import unittest
from main import create_app
from config import TestConfig
from exts import db
from models import Recipe


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig) #creates an instance of the application using a test configuration
        self.client = self.app.test_client(self) #allows to simulate requests to my API without running server        

        with self.app.app_context():
            #db.init_app(self.app)
            
            db.create_all()
            
    def test_hello_world(self):
        hello_response = self.client.get('/recipe/hello')
        
        json = hello_response.json
        
        #print(json)
        
        self.assertEqual(json,{"message":"Hello World!"})
        
        
    def test_signup(self):
        signup_response = self.client.post('/auth/signup',json = {
            "username":"testuser",
            "email":"testemail@gmail.com",
            "password":"password"
        })
        
        status_code = signup_response.status_code
        
        self.assertEqual(status_code, 201)  
        
        
    def test_login(self):
        signup_response = self.client.post(
            '/auth/signup',
            json = {
            "username":"testuser",
            "email":"testemail@gmail.com",
            "password":"password"
        })
        
        
        login_response = self.client.post(
            '/auth/login',
            json = {
            "username":"testuser",
            "password":"password"
        })          
        
        status_code = login_response.status_code
        
        json = login_response.json
        
        #print(json)
        
        self.assertEqual(status_code,200)
        
        
    def test_get_all_recipes(self):
        """Test for getting all recipes"""
        
        get_all_response = self.client.get('/recipe/recipes')
        
        json = get_all_response.json
        
        #print(json)
        
        status_code = get_all_response.status_code
        
        self.assertEqual(status_code,200)
    
    def test_get_one_recipe(self):
        id = 1
        get_one_response = self.client.get(f"/recipe/recipe{id}")
        
        json = get_one_response.json
        
        #print(json)
        
        status_code = get_one_response.status_code
        
        print(status_code)
        
        self.assertEqual(status_code,404)
        
    
    def test_create_recipe(self):
        signup_response = self.client.post(
            '/auth/signup',
            json = {
            "username":"testuser",
            "email":"testemail@gmail.com",
            "password":"password"
        })
        
        
        login_response = self.client.post(
            '/auth/login',
            json = {
            "username":"testuser",
            "password":"password"
        })
        
        print(login_response.json)
        
        
    
    def test_update_recipe(self):
        pass
    
    def test_delete_recipe(self):
        pass
    
    def tearDown(self):
        """
        Clean up after each test
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
if __name__== "__main__":
    unittest.main()
    