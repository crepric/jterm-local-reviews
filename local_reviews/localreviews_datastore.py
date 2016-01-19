#!/usr/bin/env python
import webapp2
import logging
from google.appengine.ext import ndb
import re

class Review(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    title = ndb.StringProperty(required = True)
    # TextProperty is not indexed by default, but we can make it explicit
    description = ndb.TextProperty(indexed = False)
    # We don't use the choices property for category, to make it easier to
    # add new categories in the future.
    category = ndb.StringProperty()
    # It's here but unused at the moment, we will learn how to store images
    # soon.
    image = ndb.BlobProperty()
    # An alternative to store the image itself in here, is to store a link to
    # an image file hosted elsewhere.
    image_link = ndb.StringProperty()
    # It's important to store this as an IntegerProperty, because this way we
    # are instructing Datastore on how the index for this property should be
    # built
    user_likes = ndb.IntegerProperty()
    # Amenities is a repeated property. Like category, we don't fix the possible
    # Choices so we can add new ones dynamicly.
    amenities = ndb.StringProperty(repeated=True)

    @classmethod
    def GetUserLikes(cls, key):
        key = ndb.Key(urlsafe = key)
        entry = key.get()
        if entry:
            return entry.user_likes

# This is the handler to load an image stored in a Review entity.
# The request comes as /getimg/<entity_key>, and is separated by means of
# regular expressions grouping in the "app" component at the end of this file.
# The <entity_key> is passed in as an argument, since we used grouping in the
# definition of app.
class ViewPhotoHandler(webapp2.RequestHandler):
    def get(self, review_key):
        # Step 1: let's get the entity.
        review_normalized_key = ndb.Key(urlsafe=review_key)
        review = review_normalized_key.get()
        # Step 2: if the entity has an image, send it.
        if hasattr(review, 'image'):
            # We must specify the type of file we are sending. In this app,
            # for simplicity, we will assume only png, but we could have stored
            # info on the file type in a separate property in Datastore, to be
            # more flexible.
            self.response.headers['Content-Type'] = 'image/png'
            self.response.write(review.image)

# Handler that will take care of receiving and saving a new review
class SaveReviewHandler(webapp2.RequestHandler):
    # The advantage of a post handler for the form is that we can upload
    # arbitrarily large chunks of information, such as images.
    def post(self):
        place_name = self.request.get('place_name')
        category = self.request.get('category')
        description = self.request.get('description')
        review_img_link = self.request.get('review_img_link')
        image = None
        if self.request.get('review_img'):
            image = self.request.get('review_img')
        amenities = []
        # Let's find all the attributes whose key looks like "amenities-.*"
        for key,value in self.request.POST.items():
            re_obj = re.search(r'^amenity-(.*)',key)
            if re_obj and value == "on":
                amenities.append(str(re_obj.group(0)))
        # First thing for a new review should be check for duplicates
        # We will check for Restaurant AND Category, so that two places with the
        # same name but belonging to different categories can be safely stored.
        # This is the kind of behavior that we would want to test with a unit
        # test.
        if place_name and category:
            search_review = Review.query(Review.title == place_name, Review.category == category)
            results = search_review.fetch()
            if results:
                logging.warning("We have already an entry of type %s named %s. Skipping." % (category, place_name))
            else:
                new_review = Review(
                    title = place_name,
                    description = description,
                    category = category,
                    # can be empty
                    image_link = review_img_link,
                    image = image,
                    user_likes = 1,
                    amenities = amenities
                )
                new_review.put()
        else:
            # This should also be validated in the client before sending the request.
            logging.warning("Ignoring request because it has no place_name or category")
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/save-review', SaveReviewHandler),
    # Anything that looks like /getimg/<something> will be accepted.
    # /getimg/ with nothing attached will not since it has nothing after getimg/
    ('/getimg/(.+)', ViewPhotoHandler),
], debug=True)
