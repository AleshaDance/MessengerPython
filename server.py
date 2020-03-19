import time  # +
from datetime import datetime  # наст. время
from flask import Flask, request

app = Flask(__name__)
# массив с сообщениями
messages = [  # список сообщений
    {'username': 'Alesha', 'time': time.time(), 'text': 'Qq'},
    {'username': 'Masha', 'time': time.time(), 'text': 'Hi'},
]
users = {  # словарь пользователей
    "Alesha": "qwerty",
    "Masha": "12345",
}


@app.route("/")  # Окно приветствия
def hello_view():
    return "Server running"


@app.route("/status")  # статус сервера
def status_view():
    return {
        'status': True,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'messages_count': len(messages),
        'users_count': len(users)
    }


@app.route("/messages")  # метод получения списка сообщений
def messages_view():
    """
    :input: ?after=float
    :return: [{'username': str, 'time': float, 'text': str}, ...]
    """
    print(request.args)
    after = float(request.args['after'])

    filtered_messages = []
    for message in messages:
        if message['time'] > after:
            filtered_messages.append(message)

    return {'messages': filtered_messages}


# метод отправки сообщений
@app.route("/send", methods=['POST'])  # принимаем только пост запросы
def send_view():
    """
    Отправить сообщение всем
    :input: {"username": str, "password": str, "text": str}
    :return: {"ok": bool}
    """
    print(request.json)
    username = request.json["username"]
    password = request.json["password"]
    text = request.json["text"]

    if username not in users or users[username] != password:  # если не содержится в польз-ях и паролях,доступ запрещен
        return {'ok': False}

    messages.append({'username': username, 'time': time.time(), 'text': text})
    return {'ok': True}

# залогиниться
@app.route("/login", methods=['POST'])  # принимаем только пост запросы
def login_view():
    """
    Отправить сообщение всем
    input: {"username": str, "password": str}
    :return: {"ok": bool}
    """
    print(request.json)
    username = request.json["username"]
    password = request.json["password"]

    if username not in users:
        users[username] = password
        return {'ok': True}
    elif users[username] == password:
        return {'ok': True}
    else:
        return {'ok': False}


if __name__ == '__main__':
    app.run()

