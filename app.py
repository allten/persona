# flaskから ページのレンダリングモジュールのrender_templateをロード
# flask-socketioから SocketIO, room関係のモジュールをロード

from flask import Flask, render_template, redirect, url_for, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired

# Flaskの初期化、シークレットキーの指定を行う。

app = Flask(__name__)
app.config["SECRET_KEY"] = "1@3$5s^7S"
socketio = SocketIO(app)

# メインページ(index)ページでは、GET,POSTメソードを使用し、render_templateモジュールでmain.htmlをロードする。

class LoginForm(FlaskForm):
    # name = StringField('Name', validators=[InputRequired()])
    room = StringField('Room', validators=[InputRequired()])
    submit = SubmitField('Enter Chatroom')

@app.route("/", methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        # session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for("chat"))
    elif request.method == 'GET':
        # form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('main.html', form=form, errors=form.errors.items())


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    # name = session.get('name', '')
    room = session.get("room", '')
    if room == '':
        return redirect(url_for("index"))
    return render_template('chat.html', room=room)

@socketio.on("message")
def handle_messages(json, methods=['GET', 'POST']):
    print("received my event: " + str(json))
    socketio.emit("response", json, callback=messageReceived)

@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)