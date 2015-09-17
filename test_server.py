#! /usr/bin/env python
#
# Copyright (c) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

from flask import Flask, render_template, Response, request
from flask.ext.socketio import SocketIO

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
port = 5050


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def on_connect(message):
    print(">>>>{}".format(message))


@app.route('/update_log/', methods=['GET'])
def update_log():
    source = request.args['source']
    status = request.args['status']
    message = request.args['message']
    print('Emmit from {} message "{}"'.format(source, message))
    socketio.emit('update log', {'source': source, 'message': message, 'status': status})
    return Response(message)

if __name__ == '__main__':
    from socketio.server import SocketIOServer
    SocketIOServer(('0.0.0.0', port), app,
                   resource="socket.io", policy_server=False).serve_forever()
