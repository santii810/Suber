from google.appengine.ext import ndb


class Viaje(ndb.Model):
    origen = ndb.StringProperty(required=True)
    destino = ndb.StringProperty(required=True)
    horaSalida = ndb.StringProperty(required=True)
    duracion = ndb.IntegerProperty(required=True)
    plazas = ndb.IntegerProperty(required=True)
    modelo = ndb.StringProperty(required=True)
    color = ndb.StringProperty(required=True)
    propietario = ndb.StringProperty(required=True)
    pasajeros = ndb.StringProperty(repeated=True)
