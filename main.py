#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
from google.appengine.api import users

from model.handlers.tripHandlers import NewTripHandler
from model.handlers.tripHandlers import RegisterTripHandler
from model.handlers.tripHandlers import ListTripsHandler
from model.handlers.tripHandlers import DeleteTripHandler
from model.handlers.tripHandlers import ModifyTripHandler
from model.handlers.tripHandlers import JoinTripHandler
from model.handlers.tripHandlers import ConfirmModifyTripHandler

from model.handlers.logoutHandler import LogoutHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == None:
            self.redirect(users.create_login_url("/"))

        logout_link = users.create_logout_url("/logout")
        template_values = {
            "user": user,
            "logout_link": logout_link,
        }

        template = JINJA_ENVIRONMENT.get_template("index.html")
        self.response.write(template.render(template_values));


app = webapp2.WSGIApplication(
    [('/', MainHandler),
     ('/newTrip', NewTripHandler),
     ('/registerTrip', RegisterTripHandler),
     ('/listTrips', ListTripsHandler),
     ('/logout', LogoutHandler),
     ('/deleteTrip', DeleteTripHandler),
     ('/modifyTrip', ModifyTripHandler),
     ('/confirmModifyTrip', ConfirmModifyTripHandler),
     ('/join', JoinTripHandler),

     ],
    debug=True)
