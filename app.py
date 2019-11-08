import json
import datetime
import time
import collections

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_object(__name__)

class chat(object):
    def backlog(self, size=25):
        return self.messages[-size:]

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
            backlog = active_room_backlog
            if message is None:
                break

            datetime_now = datetime.datetime.now()
            data = {
                'time': str(datetime_now.strftime('%Y年%m月%d日 %H:%M:%S')),
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
    server = WSGIServer(('localhost', 8080), app, handler_class=WebSocketHandler)
    server.serve_forever()