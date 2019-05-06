import webapp2
from webapp2_extras import jinja2
from model.viaje import Viaje
from time import sleep
from google.appengine.api import users
from google.appengine.ext import ndb


def manageUsers(self):
    user = users.get_current_user()

    if user == None:
        self.redirect(users.create_login_url("/"))
    logout_link = users.create_logout_url("/logout")

    template_values = {
        "user": user,
        "logout_link": logout_link,
    }
    return template_values


class NewTripHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)

        template_values = manageUsers(self)
        self.response.write(
            jinja.render_template("newTrip.html", **template_values));


class RegisterTripHandler(webapp2.RequestHandler):
    def load_input(self):
        self.origen = self.request.get("origen", "null")
        self.destino = self.request.get("destino", "null")
        self.horaSalida = self.request.get("horaSalida", "null")
        self.duracion = int(self.request.get("duracion", "null"))
        self.plazas = int(self.request.get("plazas", "null"))
        self.modelo = self.request.get("modelo", "null")
        self.color = self.request.get("color", "null")

    def post(self):
        jinja = jinja2.get_jinja2(app=self.app)
        template_values = manageUsers(self)

        self.load_input()

        viaje = Viaje(origen=self.origen,
                      destino=self.destino,
                      horaSalida=self.horaSalida,
                      duracion=self.duracion,
                      plazas=self.plazas,
                      modelo=self.modelo,
                      color=self.color
                      )
        viaje.propietario = template_values["user"].nickname()
        viaje.pasajeros = [viaje.propietario]
        viaje.pasajeros+= "santi"
        viaje.put()
        sleep(1)

        viajes = Viaje.query()
        template_values['viajes'] = viajes

        self.response.write(
            jinja.render_template("listTravels.html", **template_values));


class ListTripsHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        template_values = manageUsers(self)

        viajes = Viaje.query()

        template_values['viajes'] = viajes:

        self.response.write(
            jinja.render_template("listTravels.html", **template_values));


class DeleteTripHandler(webapp2.RequestHandler):
    def get(self):
        template_values = manageUsers(self)  # test user is logged and get their attributes
        id = self.request.get('id')
        selectedTrip = ndb.Key(urlsafe=id).get()
        selectedTrip.key.delete()

        sleep(1)
        jinja = jinja2.get_jinja2(app=self.app)

        viajes = Viaje.query()

        template_values['viajes'] = viajes

        self.response.write(
            jinja.render_template("listTravels.html", **template_values));


class ModifyTripHandler(webapp2.RequestHandler):
    def get(self):
        template_values = manageUsers(self)  # test user is logged and get their attributes
        id = self.request.get('id')
        selectedTrip = ndb.Key(urlsafe=id).get()
        jinja = jinja2.get_jinja2(app=self.app)

        template_values['trip'] = selectedTrip

        self.response.write(
            jinja.render_template("modifyTrip.html", **template_values));


class ConfirmModifyTripHandler(webapp2.RequestHandler):
    def post(self):
        jinja = jinja2.get_jinja2(app=self.app)
        template_values = manageUsers(self)

        id = self.request.GET['id']
        viaje = ndb.Key(urlsafe=id).get()

        viaje.origen = self.request.get("origen").strip()
        viaje.destino = self.request.get("destino").strip()
        viaje.horaSalida = self.request.get("horaSalida").strip()
        viaje.duracion = int(self.request.get("duracion").strip())
        viaje.plazas = int(self.request.get("plazas").strip())
        viaje.modelo = self.request.get("modelo").strip()
        viaje.color = self.request.get("color").strip()
        viaje.propietario = template_values["user"].nickname()

        viaje.put()
        sleep(1)

        viajes = Viaje.query()
        template_values['viajes'] = viajes

        self.response.write(
            jinja.render_template("listTravels.html", **template_values));


class JoinTripHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        template_values = manageUsers(self)

        id = self.request.GET['id']
        viaje = ndb.Key(urlsafe=id).get()

        viaje.pasajeros += template_values['user'].nickname()

        viaje.put()
        sleep(1)

        viajes = Viaje.query()
        template_values['viajes'] = viajes

        self.response.write(
            jinja.render_template("listTravels.html", **template_values));
