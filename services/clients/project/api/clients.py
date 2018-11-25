# services/clients/project/api/clients.py

from flask import Blueprint, jsonify, request, render_template

from project.api.models import Cliente
from project import db

from sqlalchemy import exc


clients_blueprint = Blueprint('clients', __name__, template_folder='./templates')


@clients_blueprint.route('/clients/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'pong!!!'
    })


@clients_blueprint.route('/clients', methods=['POST'])
def add_cliente():
    post_data = request.get_json()
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Datos no validos.'
    }
    if not post_data:
        return jsonify(response_object), 400
    nombre = post_data.get('nombre')
    apellidos = post_data.get('apellidos')
    dni = post_data.get('dni')
    sexo = post_data.get('sexo')
    celular = post_data.get('celular')
    email = post_data.get('email')
    try:
        client = Cliente.query.filter_by(nombre=nombre).first()
        if not client:
            db.session.add(Cliente(nombre=nombre, apellidos=apellidos, dni=dni, sexo=sexo, celular=celular, email=email))
            db.session.commit()
            response_object['estado'] = 'satisfactorio'
            return jsonify(response_object), 201
        else:
            
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@clients_blueprint.route('/clients/<client_id>', methods=['GET'])
def get_single_client(client_id):
    """Obteniendo detalles de un unico usuario"""
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Usuario no existe'
    }

    try:
        client = Cliente.query.filter_by(id=int(client_id)).first()
        if not client:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': client.id,
                    'nombre': client.nombre,
                    'apellidos': client.apellidos,
                    'dni': client.dni,
                    'sexo': client.sexo,
                    'celular': client.celular,
                    'email': client.email
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@clients_blueprint.route('/clients', methods=['GET'])
def get_all_clientes():
    """Get all users"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'clients': [Client.to_json() for Client in Cliente.query.all()]
        }
    }
    return jsonify(response_object), 200


@clients_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        dni = request.form['dni']
        sexo = request.form['sexo']
        celular = request.form['celular']
        email = request.form['email']
        db.session.add(Cliente(nombre=nombre, apellidos=apellidos, dni=dni, sexo=sexo, celular=celular, email=email))
        db.session.commit()
    clients = Cliente.query.all()
    return render_template('index.html', clients=clients)
