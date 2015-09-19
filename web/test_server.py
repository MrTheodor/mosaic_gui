#! /usr/bin/env python
#
# Copyright (c) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

import cPickle
import socket

from flask import Flask, render_template, Response, request, send_file
from flask.ext.socketio import SocketIO

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
port = 5050

try:
    daemon_host = open('../daemon/hostname').read().strip()
    print('Daemon host: {}'.format(daemon_host))
except:
    daemon_host = None

DAEMON_FILES = '../daemon/files'


@app.route('/')
def index():
    """Renders the index page."""
    return render_template('index.html')


@socketio.on('connect')
def on_connect(message):
    print("on_connect: {}".format(message))


@socketio.on('create_mosaic')
def on_create_mosaic(data):
    """Notify daemon with e-mail and search tag. The snapshot to process is already stored in
    snapshot.jpg. Daemon will notify gui when it finished.
    """
    print('on_data: {}'.format(data))
    if daemon_host is not None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host, port = daemon_host.split(':')
        sock.sendto(cPickle.dumps(data), (host, int(port)))
    else:
        print('No daemon defined')


@app.route('/update_log/', methods=['GET'])
def update_log():
    """Updates log on web page.

    GET args:
        source: The id of source node.
        status: The status of source node.
        message: The string with message.
    """
    source = request.args['source']
    status = request.args.get('status', '')
    message = request.args.get('message', '')
    print('Emmit from {} message "{}"'.format(source, message))
    socketio.emit('update log', {'source': source, 'message': message, 'status': status})
    return Response(message)


@app.route('/get_file/<filename>')
def get_snapshot(filename):
    """Returns snapshot.jpg."""
    return send_file('{}/{}'.format(DAEMON_FILES, filename), mimetype='image/jpeg')


@app.route('/finished/')
def finished():
    """Daemon finished. Emit signal to gui."""
    socketio.emit('finished', {'filename': request.args['filename']})
    return Response('OK')


if __name__ == '__main__':
    from socketio.server import SocketIOServer
    SocketIOServer(('0.0.0.0', port), app,
                   resource="socket.io", policy_server=False).serve_forever()
