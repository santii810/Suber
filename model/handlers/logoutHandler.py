import webapp2
from webapp2_extras import jinja2
from model.viaje import Viaje
from webapp2_extras import jinja2
from model.viaje import Viaje
from time import sleep


class LogoutHandler(webapp2.RequestHandler):

    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        self.response.write(
            jinja.render_template("logout.html"));
