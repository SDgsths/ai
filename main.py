from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import random

app = Flask(__name__)
app.secret_key = 'secret_key_for_sessions'
socketio = SocketIO(app)

# Route for the home page (Login/Join)
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        room = request.form['room']
        session['username'] = username
        session['room'] = room
        return redirect(url_for('chat'))
    return render_template('index.html')

# Route for the chat page
@app.route("/chat")
def chat():
    username = session.get('username', '')
    room = session.get('room', '')
    if username == '' or room == '':
        return redirect(url_for('index'))
    return render_template('chat.html', username=username, room=room)

# SocketIO event handler for messages
@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    emit('receive_message', data, room=room)

# SocketIO event for joining a room
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('receive_message', {'msg': f'{username} has joined the room.'}, room=room)

# SocketIO event for leaving a room
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('receive_message', {'msg': f'{username} has left the room.'}, room=room)

if __name__ == "__main__":
    socketio.run(app, debug=True)
