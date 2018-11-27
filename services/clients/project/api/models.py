from sqlalchemy.sql import func

from project import db


class Cliente(db.Model):

    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), nullable=False)
    apellidos = db.Column(db.String(128), nullable=False)
    dni = db.Column(db.String(128), nullable=False)
    sexo = db.Column(db.String(128), nullable=False)
    celular = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'dni': self.dni,
            'sexo': self.sexo,
            'celular': self.celular,
            'email': self.email
        }

    def __init__(self, nombre, apellidos, dni, sexo, celular, email):
        self.nombre = nombre
        self.apellidos = apellidos
        self.dni = dni
        self.sexo = sexo
        self.celular = celular
        self.email = email
