from flask import Flask, render_template, redirect, request, session, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)

users = {}  

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username:
            session['username'] = username
            users[username] = True
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])

@socketio.on('message')
def handle_message(msg):
    username = session.get('username', 'Anonymous')
    emit('message', {'user': username, 'msg': msg}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
