# services/users/project/tests/test_users.py

from project import db
from project.api.models import Cliente

import json
import unittest

from project.tests.base import BaseTestCase


def add_cliente(nombre, apellidos, dni, sexo, celular, email):
    clien = Cliente(nombre=nombre, apellidos=apellidos, dni=dni, sexo=sexo, celular=celular, email=email)
    db.session.add(clien)
    db.session.commit()
    return clien


class TestClienteService(BaseTestCase):
    """Prueba para el servicio users."""

    def test_clients(self):
        """Asegurando que la ruta /ping se comporta correctamente."""
        response = self.client.get('/clients/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!!!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])

    def test_add_cliente(self):
        """Asegurando de que se pueda agregar un nuevo cliente a la base de datos."""
        with self.client:
            response = self.client.post(
                '/clients',
                data=json.dumps({
                    'nombre': 'abel',
                    'apellidos': 'abel huanca',
                    'dni': '51452452',
                    'sexo': 'F',
                    'celular': '985224855',
                    'email': 'abel.huanca@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
           

    def test_add_cliente_invalid_json(self):
        """Asegurando de que se arroje un error si el objeto json esta
        vacio."""
        with self.client:
            response = self.client.post(
                '/clients',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_cliente_invalid_json_keys(self):
        """
        Asegurando de que se produce un error si el objeto JSON no tiene
        un key de nombre de usuario.
        """
        with self.client:
            response = self.client.post(
                '/clients',
                data=json.dumps({'nombre': 'abel'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_cliente_duplicate_email(self):
        """Asegurando de que se produce un error si el correo electronico ya
        existe."""
        with self.client:
            self.client.post(
                '/clients',
                data=json.dumps({
                    'nombre': 'abel',
                    'apellidos': 'abel huanca',
                    'dni': '51452452',
                    'sexo': 'F',
                    'celular': '985224855',
                    'email': 'abel.huanca@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/clients',
                data=json.dumps({
                    'nombre': 'abel',
                    'apellidos': 'abel  huanca',
                    'dni': '51452452',
                    'sexo': 'F',
                    'celular': '985224855',
                    'email': 'abel.huanca@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            

    def test_single_cliente(self):
        """Asegurando de que el usuario individual se comporte
        correctamente."""
        clients = add_cliente('abel', 'abel  huanca', '51452452', 'F', '985224855', 'abel.huanca@upeu.edu.pe')
        with self.client:
            response = self.client.get(f'/clients/{clients.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('abel', data['data']['nombre'])
            self.assertIn('abel  huanca', data['data']['apellidos'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_cliente_no_id(self):
        """Asegurando de que se lanze un error si no se proporciona un id."""
        with self.client:
            response = self.client.get('/clients/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)

    def test_single_cliente_incorrect_id(self):
        """Asegurando de que se lanze un error si el id no existe."""
        with self.client:
            response = self.client.get('/clients/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)

    def test_all_clients(self):
        """Asegurarse de que todos los usuarios se comporte correctamente."""
        add_cliente('abel', 'abel  huanca', '51452452', 'F', '985224855', 'abel.huanca@upeu.edu.pe')
        add_cliente('zosimo', 'santos gutarra', '5645674', 'F', '985224855', 'zosimo.huanca@upeu.edu.pe')
        with self.client:
            response = self.client.get('/clients')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['clients']), 2)
            self.assertIn('abel', data['data']['clients'][0]['nombre'])
            self.assertIn(
                'abel  huanca', data['data']['clients'][0]['apellidos'])
            self.assertIn('zosimo', data['data']['clients'][1]['nombre'])
            self.assertIn(
                'santos gutarra', data['data']['clients'][1]['apellidos'])
            self.assertIn('satisfactorio', data['estado'])

    def test_main_no_cliente(self):
        """Ensure the main route behaves correctly when no users have been
        added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_with_cliente(self):
        """Ensure the main route behaves correctly when users have been
        added to the database."""
        add_cliente('abel', 'abel  huanca', '51452452', 'F', '985224855', 'abel.huanca@upeu.edu.pe')
        add_cliente('zosimo', 'santos gutarra', '5645674', 'F', '985224855', 'zosimo.huanca@upeu.edu.pe')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_main_add_cliente(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(nombre='abel', apellidos='pongo ', dni='71545511', sexo='M', celular='55555653', email='abel.huanca@upeu.edu.pe'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
