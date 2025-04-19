import unittest
import psycopg2
from main import app
import json

class FlaskTestCase1(unittest.TestCase): #Работает
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        connection = psycopg2.connect(database='Orders_organization', user='administrator', password='root', host='localhost', port='5432')
        cursor  = connection.cursor()

        cursor.execute('''Drop table if exists Orders;

                    Create table Orders(
                    order_id int primary key not null,
                    order_status varchar(32) not null
                    );''')

        connection.commit()
        connection.close()
        cursor.close()

    def test_orders_get(self):
        '''Тест GET-Запроса'''
        response = self.app.get('/orders')
        self.assertEqual(response.status_code, 200)

    def test_orders_post(self):
        """Тест POST-запроса с JSON"""
        response = self.app.post('/orders',
                                 data=json.dumps({'id': 0, 'desc': 'Created'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, [[0, 'Created']])

class FlaskTestCase2(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        connection = psycopg2.connect(database='Orders_organization', user='administrator', password='root', host='localhost', port='5432')
        cursor  = connection.cursor()

        cursor.execute('''Drop table if exists Orders;

                    Create table Orders(
                    order_id int primary key not null,
                    order_status varchar(32) not null
                    );''')
        
        cursor.execute('''INSERT INTO Orders(order_id, order_status)
                   VALUES (%s, %s);''', (0, 'Created'))

        connection.commit()
        connection.close()
        cursor.close()

    def test_orders_id_get(self):
        '''Тест GET-Запроса'''
        response = self.app.get(f'/orders/{0}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [[0, 'Created']])

    def test_orders_update(self):
        '''Тест PUT-Запроса'''
        response = self.app.put(f'/orders/{0}', data=json.dumps({'desc': 'REDACTED'}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Message': f'Order with id: {0} updated successfully'})

class FlaskTestCase3(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        connection = psycopg2.connect(database='Orders_organization', user='administrator', password='root', host='localhost', port='5432')
        cursor  = connection.cursor()
        cursor.execute('''Drop table if exists Orders;

                    Create table Orders(
                    order_id int primary key not null,
                    order_status varchar(32) not null
                    );''')
        
        cursor.execute('''INSERT INTO Orders(order_id, order_status)
                VALUES (%s, %s)''', (0, 'Created'))    
        
        connection.commit()
        connection.close()
        cursor.close()

    def test_orders_delete(self):
        response = self.app.delete(f'/orders/{0}',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Message': f'Order with id: {0} deleted successfully'})

if __name__ == '__main__':
    unittest.main()