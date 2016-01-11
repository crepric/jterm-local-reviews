import unittest
import webapp2

# from the app main.py
import main

class TestHandlers(unittest.TestCase):
    def testMainpage(self):
       # Build a request object passing the URI path to be tested.
       # You can also pass headers, query arguments etc.
       request = webapp2.Request.blank('/')
       # Get a response for that request.
       response = request.get_response(main.app)

       # Let's check if the response is correct.
       self.assertEqual(response.status_int, 200)
       self.assertIn('Northampton Local Guide', response.body)


if __name__ == '__main__':
    unittest.main()
