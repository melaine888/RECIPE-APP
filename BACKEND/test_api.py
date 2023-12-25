import unittest
from main import create_app
from config import TestConfig
from exts import db


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
        
        #print(status_code)
        
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
        
        #access_token = login_response.json["access_token"]
        
        for item in login_response.json:
            if "access_token" in item:
                access_token = item["access_token"]
                #print(access_token)
                break 

        create_recipe_response = self.client.post(
            '/recipe/recipes',
            json = {
            "title":"Test cookie",
            "description":" Test description"
        },
                                                  
            headers = {
                "Authorization header":f"Bearer{access_token}"
            })
        
        status_code = create_recipe_response.status_code
        
        #print(create_recipe_response.json)
        
        self.assertEqual(status_code,201)
        
    
    def test_update_recipe(self):
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
        
        #access_token = login_response.json["access_token"]
        
        for item in login_response.json:
            if "access_token" in item:
                access_token = item["access_token"]
                #print(access_token)
                break 

        create_recipe_response = self.client.post(
            '/recipe/recipes',
            json = {
            "title":"Test cookie",
            "description":" Test description"
        },
                                                  
            headers = {
                "Authorization header":f"Bearer{access_token}"
            })
        
        status_code = create_recipe_response.status_code
        
        #id = 1
        
        updated_response = self.client.put(
            f"/recipe/recipe/{id}",
            json = {
                "title":"Test cookie updated",
                "description":"Test description"
            },
            headers = {
                "Authorization":f"Bearer {access_token}"
            }
        )
        
        status_code = updated_response.status_code
        
        #print(updated_response.json)
        
        self.assertEqual(status_code, 404)
        
    
    def test_delete_recipe(self):
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
        
        #access_token = login_response.json["access_token"]
        
        for item in login_response.json:
            if "access_token" in item:
                access_token = item["access_token"]
                #print(access_token)
                break 

        create_recipe_response = self.client.post(
            '/recipe/recipes',
            json = {
            "title":"Test cookie",
            "description":" Test description"
        },
                                                  
            headers = {
                "Authorization header":f"Bearer{access_token}"
            })
        
        deleted_response = self.client.delete(
            f'/recipe/recipe/{id}',
            headers = {
                "Authorization":f"Bearer{access_token}"
            })
        
        status_code = deleted_response.status_code

        print(deleted_response.json)

        self.assertEqual(status_code, 404)
    
    def tearDown(self):
        """
        Clean up after each test
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
if __name__== "__main__":
    unittest.main()
    