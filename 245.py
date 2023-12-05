from flask import Flask, request, Response
import uuid
import time

app = Flask(__name__)

users = {}
name = ""
text = ""
msg = []

@app.route('/')
def main():
    return "commands /auth, /send, /logout, /getall"

@app.route('/auth')
def auth():
    global name
    name = request.args.get('name')
    if name not in users:
        token = uuid.uuid4()
        users[name] = token
        print(users)
        return f"Вы успешно авторизовались ваш токен - {token}"
    else:
        return "Такой пользователь уже есть"

@app.route('/send')
def send():
    global name
    global text
    text = request.args.get('text')
    tok = request.args.get('tok')
    count = 0
    for symbols in tok:
        count += 1

    if text is None:
        return 'Текст не указан'
    elif tok is None:
        return "Токен не указан"
    elif count < 36:
        return "Токен невереный"
    else:
        if name is not None:
            timestamp = time.time()
            msg.append({'name': name, 'text': text, 'time': timestamp})
            return Response("Сообщение отправлено", status=200, mimetype="text/plain")
        else:
            return Response("Имя пустое", status=403, mimetype="text/plain")

@app.route("/logout")
def logout():
    global name
    name = ""
    return 'logout'

@app.route('/getall')
def getall():
    return str(msg)

if __name__ == '__main__':
    app.run(debug=True)
