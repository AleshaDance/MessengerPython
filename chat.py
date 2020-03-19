import threading
from datetime import datetime
from time import sleep

import requests
from PyQt5 import QtWidgets  # class widgets
from PyQt5.QtWidgets import QDialog
from mainQT import Ui_MainWindow  # импортирует Ui_MainWindow
from dialogQT import Ui_Dialog as TableDialog


class DialogTable(QDialog, TableDialog):
    def __init__(self):
        super().__init__()  # вызывает метод init
        self.setupUi(self)  # вызываем ф-ю
        self.pushButton.clicked.connect(self.registration)  # клик
        self.pushButton.clicked.connect(self.login)  # клик
        self.username = 'Jack'
        self.password = 'Black'

    def registration(self):
        self.username = self.lineEdit.text()
        self.password = self.lineEdit_2.text()

    def login(self):
        self.username = self.lineEdit.text()
        self.password = self.lineEdit_2.text()


# КЛАСС НАСЛЕДОВАНИЯ
class OurApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):  # __ __ фу-я, вывзывает все остальные ф-ии
        super().__init__()  # вызывает метод init
        self.setupUi(self)  # вызываем ф-ю
        self.pushButton.clicked.connect(self.send)  # клик
        threading.Thread(target=self.receive).start()

    # ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЯ
    def send(self):
        text = self.lineEdit.text()  # выводит текст в консоль
        username = DialogTable().username
        password = DialogTable().password
        # выводим возможные ошибки
        try:
            response = requests.post('http://127.0.0.1:5000/login',json={
                'username': username,
                'password': password
            })
            print(response.text)
            response = requests.post('http://127.0.0.1:5000/send',json={
                'username': username,
                'password': password,
                'text': text
            })
            print(response.text)
        except requests.exceptions.ConnectionError:
            print('Сервер недоступен')
            return
        except:
            print('Какая-то ошибка произошла')
            return

        self.lineEdit.setText('')  # текст в send исчезает
        self.lineEdit.repaint()  # перерисовывает и очищает поле

    # ФУНКЦИЯ ПОЛУЧЕНИЯ СООБЩЕНИЯ
    def receive(self):
        last_time = 0
        while True:  # подгрузить все сообщения
            try:
                response = requests.get('http://127.0.0.1:5000/messages',
                                        params={'after': last_time})
            except:
                print('Сервер отключен')
                sleep(1)
                continue

            # сообщения после опред-й метки (обновл-я)
            for message in response.json()['messages']:  # выводит все сообщения
                time_format = datetime.fromtimestamp(message['time'])
                time_format = time_format.strftime('%Y-%m-%d %H:%M:%S')
                header = message['username'] + ' в ' + time_format
                text = message['text']

                if text != "":  # and message['username'] != ""
                    self.textBrowser.append(header)  # добавляем текст
                    self.textBrowser.append(text)
                    self.textBrowser.append('')

                last_time = message['time']
            sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = OurApp()
    dialog = DialogTable()
    window.show()
    dialog.show()
    app.exec_()
