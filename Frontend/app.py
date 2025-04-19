from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import requests

def error_show(error_information):
    error = QMessageBox()
    error.setWindowTitle("Ошибка")
    error.setText('Ошибка: ' + str(error_information))
    error.setIcon(QMessageBox.Warning)
    error.setStandardButtons(QMessageBox.Ok)
    error.exec_()

def success_show(success_information):
    success = QMessageBox()
    success.setWindowTitle("Успех")
    success.setText(str(success_information))
    success.setIcon(QMessageBox.Information)
    success.setStandardButtons(QMessageBox.Ok)
    success.exec()

def list_from_json(text):
    orders = []
    temp, temper, num_count = 0, 0, 0
    for i in range(len(text)):
        if num_count != 0:
            num_count -= 1
            continue
        if text[i].isdigit(): #Поиск ID
            temper = i
            while True:
                if text[temper+1].isdigit():
                    num_count +=1
                    temper += 1
                else:
                    break
            orders.append(text[i:temper+1])
            temper = 0

        if text[i] == '"': #Поиск Статуса
            if temp == 0:
                temp = i
            else:
                orders.append(text[temp:i+1])
                temp = 0
    return orders


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(824, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 271, 71))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 20, 141, 41))
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_6.setGeometry(QtCore.QRect(140, 20, 121, 41))
        self.pushButton_6.setCheckable(False)
        self.pushButton_6.setObjectName("pushButton_6")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 120, 791, 431))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(290, 10, 501, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(120, 20, 111, 41))
        self.pushButton_3.setCheckable(False)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_4.setGeometry(QtCore.QRect(230, 20, 151, 41))
        self.pushButton_4.setCheckable(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_5.setGeometry(QtCore.QRect(380, 20, 101, 41))
        self.pushButton_5.setCheckable(False)
        self.pushButton_5.setObjectName("pushButton_5")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setGeometry(QtCore.QRect(10, 70, 141, 31))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(230, 70, 251, 31))
        self.lineEdit_2.setClearButtonEnabled(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(10, 20, 101, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Приложение управления заказами"))
        self.groupBox.setTitle(_translate("MainWindow", "Действия со всеми заказами"))
        self.pushButton_2.setText(_translate("MainWindow", "Отобразить все заказы"))
        self.pushButton_6.setText(_translate("MainWindow", "Удалить все заказы"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Status"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Действия с одним заказом"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Введите номер заказа..."))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Введите статус заказа..."))
        self.pushButton.setText(_translate("MainWindow", "Добавить заказ"))
        self.pushButton_3.setText(_translate("MainWindow", "Отобразить заказ"))
        self.pushButton_4.setText(_translate("MainWindow", "Изменить статус заказа"))
        self.pushButton_5.setText(_translate("MainWindow", "Удалить заказ"))

        #Кнопки

        self.pushButton.clicked.connect(self.orders_creation)       # Добавить заказ
        self.pushButton_2.clicked.connect(self.orders_show)         # Отобразить все заказы
        self.pushButton_3.clicked.connect(self.order_show)         # Отобразить заказ
        self.pushButton_4.clicked.connect(self.order_redact)         # Изменить статус заказа
        self.pushButton_5.clicked.connect(self.order_delete)         # Удалить заказ
        self.pushButton_6.clicked.connect(self.orders_delete)         # Удалить все заказы


    def orders_creation(self):
        order_number = self.lineEdit.text()
        order_description = self.lineEdit_2.text()
        data = {'id': order_number, 'desc': order_description}
        try:
            responce = requests.post('http://127.0.0.1:5000/orders', json = data)
        except Exception as error_info:
            error_show(error_info)
        success_show('Заказ успешно создан.')
        return


    def orders_show(self):
        try:
            responce = requests.get('http://127.0.0.1:5000/orders')
        except Exception as error_info:
            error_show(error_info)
            return
        if responce.status_code == 200:
            orders = list_from_json(responce.text)
            row = 0
            self.tableWidget.setRowCount(len(orders)//2)
            for order in range(0, len(orders), 2):
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(orders[order])))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(orders[order+1]))
                row += 1
        else:
            error_show(responce.status_code)
            return
        return


    def order_show(self):
        order_number = self.lineEdit.text()
        if str(order_number).isdigit() == False or str(order_number) == "":
            error_show("Номер должен быть числом и должен быть введён.")
            return
        else:
            try:
                responce = requests.get(f'http://127.0.0.1:5000/orders/{order_number}')
            except Exception as error_info:
                error_show(error_info)
                return
            if responce.status_code == 200:
                orders = list_from_json(responce.text)
                row = 0
                self.tableWidget.setRowCount(len(orders)//2)
                for order in range(0, len(orders), 2):
                    self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(orders[order])))
                    self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(orders[order+1]))
                    row += 1
            else:
                error_show(responce.status_code)
                return
            success_show('Заказ успешно отображён.')
            return


    def order_redact(self):
        order_number = self.lineEdit.text()
        order_description = self.lineEdit_2.text()
        data = {'desc': order_description}
        if str(order_number).isdigit() == False:
            error_show("Номер должен быть числом")
        elif order_description == "":
            error_show("Описание не может быть пустым.")
            return
        else:
            try:            
                responce = requests.put(f'http://127.0.0.1:5000/orders/{order_number}', json = data)
            except Exception as error_info:
                error_show(error_info)
                return
            if responce.status_code != 200:
                error_show(responce.status_code)
                return
            success_show('Заказ успешно изменён.')
            return


    def order_delete(self):
        order_number = self.lineEdit.text()
        if str(order_number).isdigit() == False or str(order_number) == "":
            error_show("Номер должен быть числом и должен быть введён.")
            return
        else:
            try:
                responce = requests.delete(f'http://127.0.0.1:5000/orders/{order_number}')
            except Exception as error_info:
                error_show(error_info)
            success_show('Заказ успешно удалён.')
            return  


    def orders_delete(self):
        try:
            responce = requests.delete('http://127.0.0.1:5000/orders')
        except Exception as error_info:
            error_show(error_info)
            return
        success_show('Все заказы успешно удалены.')
        return

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())