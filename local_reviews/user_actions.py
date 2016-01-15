import webapp2
import logging
import localreviews_datastore as LR
from google.appengine.ext import ndb
import json

class MainHandler(webapp2.RequestHandler):
    def post(self, action):
        entry = ndb.Key(urlsafe = self.request.get('id')).get()
        if action == "voteinc":
            entry.user_likes = entry.user_likes + 1
        if action == "votedec":
            entry.user_likes = entry.user_likes - 1

        entry.put()
        response_obj = {'likes':  entry.user_likes ,
                        'review_key': entry.key.urlsafe()}
        self.response.write(json.dumps(response_obj))
        self.response.headers['Content-Type'] = "application/json"

app = webapp2.WSGIApplication([
    ('/ua/(.*)', MainHandler),
], debug=True)
