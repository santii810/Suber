import os
import jinja2
import webapp2
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class Salute(ndb.Model):
    name = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)


class SaluteHandler(webapp2.RequestHandler):

    def get_input(self):
        self.name = self.request.get("name", "pobrecito hablador")

    def post(self):
        self.get_input()

        # Get all previous answers
        salutations = Salute.query().order(Salute.time);
        # Store the answer
        salute = Salute(name=self.name);
        salute.put();
        # Prepare the answer
        template_values = {
            'name': self.name,
            'salutations': salutations,
        }
        template = JINJA_ENVIRONMENT.get_template("templates/answer.html")
        self.response.write(template.render(template_values));


app = webapp2.WSGIApplication([
    ('/hi', SaluteHandler),
], debug=True)
