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
            
    def tearDown(self):
        """
        Clean up after each test
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
if __name__== "__main__":
    unittest.main()
    