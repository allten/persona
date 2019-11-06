import json
import datetime
import time

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pipe')
def pipe():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']

        while True:
            time.sleep(1)
            message = ws.receive()
            chatname = ws.receive()
            if message is None:
                break

            datetime_now = datetime.datetime.now()
            data = {
                'time': str(datetime_now),
                'message': message,
                'chatname': chatname
            }
            ws.send(json.dumps(data))

            print(message)
            print(chatname)
            print(data)

    return


if __name__ == '__main__':
    app.debug = True

    host = '0.0.0.0'
    port = 8080
    host_port = (host, port)

    server = WSGIServer(
        host_port,
        app,
        handler_class=WebSocketHandler
    )
    server.serve_forever()