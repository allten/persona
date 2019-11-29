from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "123Fe$#"
socketio = SocketIO(app)

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template('main.html')



@app.route("/<roomname>/", methods=['GET', 'POST'])
def sessions():
    username = username
    return render_template('chat.html')

def messageReceived(methods=['GET', 'POST']):
    print('message received')

@socketio.on("joinchat")
def join_chat(methods=['GET', 'POST']):
    return redirect(url_for('/<roomname>'))




@socketio.on("message")
def handle_messages(json, methods=['GET', 'POST']):
    print("received my event: " + str(json))
    socketio.emit("response", json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)