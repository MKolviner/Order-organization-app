# 7. Crud для заказов
from flask import Flask, jsonify, request
import psycopg2
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
# Настройка
global num
connection = psycopg2.connect(database='Orders_organization', user='adminisrator', password='root', host='localhost',
                              port='5432')
cursor = connection.cursor()

cursor.execute('''SELECT COUNT(*) AS total_rows FROM Orders''')
num = cursor.fetchall()[0][0]
if num is None:
    num = 0

connection.commit()
connection.close()
cursor.close()


@app.route('/orders', methods=['POST'])
def orders_post():
    """
    Добавление нового заказа.
    ---
    tags:
      - Orders
    parameters:
      - name: id
        in: body
        type: integer
        required: false
        example: {"id":0}
        description: Идентификатор заказа (если не указан, будет использован текущий номер).
      - name: desc
        in: body
        type: string
        required: false
        example: {"desc":"Created"}
        description: Описание заказа (по умолчанию 'Created').
    responses:
      201:
        description: Заказ успешно добавлен.
      400:
        description: Ошибка при добавлении заказа.
    """
    global num
    connection = psycopg2.connect(database='Orders_organization', user='adminisrator', password='root',
                                  host='localhost', port='5432')
    cursor = connection.cursor()
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

    num += 1  # Увеличение номера на 1

    connection.commit()
    connection.close()
    cursor.close()

    return jsonify(output), 201


@app.route('/orders', methods=['GET'])
def orders_get():
    """
    Получение списка всех заказов.
    ---
    tags:
      - Orders
    responses:
      200:
        description: Список всех заказов.
      500:
        description: Ошибка при получении заказов.
    """

    connection = psycopg2.connect(database='Orders_organization', user='adminisrator', password='root',
                                  host='localhost', port='5432')
    cursor = connection.cursor()

    cursor.execute('''SELECT order_id, order_status FROM Orders ORDER BY order_id ASC''')
    output = cursor.fetchall()

    connection.commit()
    connection.close()
    cursor.close()

    return jsonify(output), 200


@app.route('/orders/<id>', methods=['GET'])
def orders_id_get(id):
    """
    Получение заказа по идентификатору.
    ---
    tags:
      - Orders
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Идентификатор заказа.

    responses:
      200:
        description: Заказ найден.
      404:
        description: Заказ не найден.

   """


    connection = psycopg2.connect(database='Orders_organization', user='adminisrator', password='root',
                                  host='localhost', port='5432')
    cursor = connection.cursor()

    try:
        cursor.execute(f'''SELECT order_id, order_status FROM Orders WHERE order_id = {id};''')
        output = cursor.fetchall()
    except Exception as e:
        return jsonify({'Message': f'Order with id {id} not found'}), 404

    if output == []:
        return jsonify({'Message': f'Order with id {id} not found'}), 404

    connection.commit()
    connection.close()
    cursor.close()

    return jsonify(output), 200


@app.route('/orders/<id>', methods=['PUT'])
def orders_update_status(id):
    """
    Обновление статуса заказа по идентификатору.
    ---
    tags:
      - Orders
    parameters:
      - name: id
        in: body
        type: integer
        required: false
        example: {"id":0}
        description: Идентификатор заказа.
      - name: desc
        in: body
        type: string
        required: false
        example: {"desc":"Redacted"}
        description: Новое описание заказа.
    responses:
      200:
        description: Заказ успешно обновлён.
      400:
        description: Описание обязательно для заполнения.
      404:
        description: Заказ не найден.
    """

    connection = psycopg2.connect(database='Orders_organization', user='adminisrator', password='root',
                                  host='localhost', port='5432')
    cursor = connection.cursor()

    data = request.get_json()
    description = data.get('desc')

    if description is None:
        return jsonify({'Message': f'Description (desc) is required'}), 400

    try:
        cursor.execute('''UPDATE orders SET order_status = %s WHERE order_id = %s;''', (description, id))
    except Exception as e:
        return jsonify({'Message': f'Order with id {id} not found'}), 404

    connection.commit()
    connection.close()
    cursor.close()

    return jsonify({'Message': f'Order with id: {id} updated successfully'}), 200


@app.route('/orders/<id>', methods=["DELETE"])
def orders_delete(id):
    """
    Удаление заказа по идентификатору.
    ---
    tags:
      - Orders
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Идентификатор заказа, который необходимо удалить.

    responses:
      200:
        description: Заказ успешно удалён.
      404:
        description: Заказ не найден.
    """
    connection = psycopg2.connect(database='Orders_organization', user='adminisrator', password='root',
                                  host='localhost', port='5432')
    cursor = connection.cursor()

    try:
        cursor.execute(f'''DELETE FROM Orders WHERE order_id = {id};''')
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
    """
    Удаление всех заказов.
    ---
    tags:
      - Orders
    responses:
      200:
        description: Все заказы успешно удалены.
    """

    connection = psycopg2.connect(database='Orders_organization', user='adminisrator', password='root',
                                  host='localhost', port='5432')
    cursor = connection.cursor()

    cursor.execute('''DELETE FROM Orders;''')

    connection.commit()
    connection.close()
    cursor.close()

    global num
    num = 0

    return jsonify({'Message': f'All orders were deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)