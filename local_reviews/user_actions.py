import webapp2
import logging
import localreviews_datastore as LR
from google.appengine.ext import ndb
import json

class UaHandler(webapp2.RequestHandler):
    def post(self, action):
        if (not self.request.get('id')):
            logging.warning ('User Action does not specify target object')
        entry = ndb.Key(urlsafe = self.request.get('id')).get()
        if action == 'voteinc':
            entry.user_likes = entry.user_likes + 1
        elif action == 'votedec':
            entry.user_likes = entry.user_likes - 1
        else:
            loggging.warning('Unhandled Action')
            self.response.write(json.dumps({}))
            return
        entry.put()
        # We return back the new counter and the ID to which it refers to.
        response_obj = {'likes':  entry.user_likes ,
                        'review_key': entry.key.urlsafe()}
        # We convert the response object to JSON notation, this is call "Serialization"
        # and allows sending an object represented as a string.
        self.response.write(json.dumps(response_obj))
        # We must specify in the HTTP header that this object is of type JSON.
        self.response.headers['Content-Type'] = "application/json"

class CountersHandler(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        logging.info(data)
        reply = []
        if data['ids']:
            for entry in data['ids']:
                likes = LR.Review.GetUserLikes(entry)
                if likes:
                    reply.append({
                        'key': entry,
                        'likes': likes,
                    })
        self.response.headers['Content-Type'] = "application/json"
        self.response.write(json.dumps(reply))


app = webapp2.WSGIApplication([
    # Accepted links are /ua/voteinc
    ('/ua/(.*)', UaHandler),
    ('/get_counters', CountersHandler),
], debug=True)
