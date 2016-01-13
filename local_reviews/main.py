#!/usr/bin/env python
import webapp2

from google.appengine.api import users
import logging
import os
import jinja2
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# Ephimeral storage for our entries. This will be reset every time the
# application restart. Any change will be lost. This is not the correct way
# to store information that can change (such as user input), but gives us
# the opportunity to test our templates
ENTRIES = [
    # Entry 1:
        {'name': 'The roost',
         'imglink': 'http://3.bp.blogspot.com/-jwhdW0tIzj8/TWQCXYSbAAI/AAAAAAAACRw/cSah99D_yHg/s1600/roost_lores-6.jpg',
         'category': 'Coffee Shop',
         'description': 'It\'s a warm and cozy coffee shop, serves breakfast, soup sandwiches',
         'user_likes': 100,
         'amenities':['WiFi', 'Heating', 'Bathroom'],
         },
    # Entry 2: - order of keys doe not matter.
         {'name': 'Local Burgers',
          'imglink': 'http://media.masslive.com/entertainment/photo/10489516-large.jpg',
          'category': 'Restaurant',
          'description': 'Hamburgers are pretty good. The fried items a bit soaky',
          'user_likes': 20,
          # Leaving amenities empty to verify that in this case a special string
          # is printed to specify that there are no amenities.
          'amenities': [],
          },
]

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template_header = JINJA_ENVIRONMENT.get_template('templates/header.html')
            template_footer = JINJA_ENVIRONMENT.get_template('templates/footer.html')
            # Start by writing the header
            self.response.write(template_header.render())
            # Fill the body
            template_values = {'username': user.nickname(),
                               'logout_link': users.create_logout_url('/'),
                               'entries': ENTRIES}
            template = JINJA_ENVIRONMENT.get_template('templates/index.html')
            self.response.write(template.render(template_values))
            # Close the page
            self.response.write(template_footer.render())
        else:
            # if the user is not logged in, let's have them log in.
            self.redirect(users.create_login_url('/'))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
