# 7. Crud для заказов
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

#Настройка
global num
connection = psycopg2.connect(database='Orders_organization', user='administrator', password='root', host='localhost', port='5432')
cursor  = connection.cursor()

cursor.execute('''SELECT COUNT(*) AS total_rows FROM Orders''')
num = cursor.fetchall()[0][0]
if num == None:
    num = 0

connection.commit()
connection.close()
cursor.close()

@app.route('/orders', methods =['POST']) #Работает
def orders_post(): #Добавление заказа
    global num
    connection = psycopg2.connect(database='Orders_organization', user='administrator', password='root', host='localhost', port='5432')
    cursor  = connection.cursor()
    data = request.get_json()
    identificator = data.get('id')
    description = data.get('desc')
    if identificator == '':
        identificator = num
    if description == '':
        description = 'Created'
    try:
        cursor.execute('''INSERT INTO Orders(order_id, order_status)
                   VALUES (%s, %s);''', (int(identificator), str(description)))
    except Exception as Error:
        print(Error)
        pass

    cursor.execute('''SELECT order_id, order_status FROM Orders''')
    output = cursor.fetchall()

    num += 1 #Увеличение номера на 1

    connection.commit()
    connection.close()
    cursor.close()
    return jsonify(output), 201


@app.route('/orders', methods=['GET']) #Работает
def orders_get(): #Выдача всех заказов, сортировка таблицы

    connection = psycopg2.connect(database='Orders_organization', user='administrator', password='root', host='localhost', port='5432')
    cursor  = connection.cursor()

    cursor.execute('''SELECT order_id, order_status FROM Orders ORDER BY order_id ASC''')
    output = cursor.fetchall()

    connection.commit()
    connection.close()
    cursor.close()
    return jsonify(output), 200



@app.route('/orders/<id>', methods=['GET']) #Работает
def orders_id_get(id):
    
    connection = psycopg2.connect(database='Orders_organization', user='administrator', password='root', host='localhost', port='5432')
    cursor  = connection.cursor()
    
    try:
        cursor.execute(f'''SELECT order_id, order_status FROM Orders
                WHERE order_id = {id};''')
        output = cursor.fetchall()
    except:
        return jsonify({'Message': f'Order with id {id} not found'}), 404
    if output == []:
        return jsonify({'Message': f'Order with id {id} not found'}), 404

    connection.commit()
    connection.close()
    cursor.close()

    return jsonify(output), 200


@app.route('/orders/<id>', methods=['PUT']) #Работает
def orders_update_status(id):

    connection = psycopg2.connect(database='Orders_organization', user='administrator', password='root', host='localhost', port='5432')
    cursor  = connection.cursor()
    
    data = request.get_json()
    description = data.get('desc')
    
    if description is None:
        return jsonify({'Message': f'Description (desc) is required'}), 400
    try:
        cursor.execute('''Update orders
                    set order_status = %s
                    where order_id = %s;;''', (description, id))
    except:
        return jsonify({'Message': f'Order with id {id} not found'}), 404

    connection.commit()
    connection.close()
    cursor.close()

    return jsonify({'Message': f'Order with id: {id} updated successfully'}), 200


@app.route('/orders/<id>', methods=["DELETE"]) #Работает
def orders_delete(id):

    connection = psycopg2.connect(database='Orders_organization', user='administrator', password='root', host='localhost', port='5432')
    cursor  = connection.cursor()
    
    try:
        cursor.execute(f'''DELETE FROM Orders
                    where order_id = {id};''')
    except:
        return jsonify({'Message': f'Order with id {id} not found'}), 404
    
    connection.commit()
    connection.close()
    cursor.close()
    global num
    num = 0
    return jsonify({'Message': f'Order with id: {id} deleted successfully'}), 200

@app.route('/orders', methods=["DELETE"])
def all_orders_delete():

    connection = psycopg2.connect(database='Orders_organization', user='administrator', password='root', host='localhost', port='5432')
    cursor  = connection.cursor()

    cursor.execute('''Delete from Orders *''')

    connection.commit()
    connection.close()
    cursor.close()

    global num
    num = 0

    return jsonify({'Message': f'All orders was deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)