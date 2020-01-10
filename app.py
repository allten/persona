from flask import Flask, render_template, redirect, url_for, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "1@3$5s^7S"
socketio = SocketIO(app)

class LoginForm(FlaskForm):
    room = StringField('Room', validators=[InputRequired()])
    submit = SubmitField('Enter Chatroom')

@app.route("/", methods=['GET','POST'])
def index():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        session['room'] = form.room.data
        return redirect(url_for(".chat"))
    elif request.method == 'GET':
        form.room.data = session.get('room', '')
    return render_template('main.html', form=form)

@app.route("/chat", methods=['GET', 'POST'])
def chat():
    room = session.get('room', '')
    if room == '':
        return redirect(url_for('index'))
    return render_template('chat.html', room=room)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on("message")
def handle_messages(json, methods=['GET', 'POST']):
    print("received my event: " + str(json))
    socketio.emit("response", json, callback=messageReceived)

@socketio.on('joined')
def join(message):
    join_room(message['room'])
    room = session.get('room')
    
    emit('status', {'msg': session.get('room') + ' has entered the room.'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)