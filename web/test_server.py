#! /usr/bin/env python
#
# Copyright (c) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.

import argparse
import cPickle
import os
import socket
import time

from flask import Flask, render_template, Response, request, send_file
from flask.ext.socketio import SocketIO

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

camera_hostname = None

@app.route('/')
def index():
    """Renders the index page."""

    # Gets last
    img_files = [f for f in os.listdir(daemon_files) if f.startswith('final')]
    img_files.sort(key=lambda x: float(x.replace('.png', '').split('_')[-1]), reverse=True)

    return render_template('index.html', jpg_files=img_files[:4], camera_hostname=camera_hostname)

@socketio.on('connect')
def on_connect():
    print "Connected to server."

@socketio.on('message')
def handle_message(msg):
    print msg 

@socketio.on('create_mosaic')
def on_create_mosaic(data):
    """Notify daemon with e-mail and search tag. The snapshot to process is already stored in
    snapshot.jpg. Daemon will notify gui when it finished.
    """
    print('data: {}'.format(data))
    if daemon_host is not None:
    	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host, port = daemon_host.split(':')
        print "making request to master: ", host, port
        sock.sendto(cPickle.dumps(data), (host, int(port)))
    else:
        print('No daemon defined')

@socketio.on('ping daemon')
def on_ping_daemon():
    """Check if daemon is ready to process mosaic otherwise block gui."""
    if daemon_host is not None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host, port = daemon_host.split(':')
        print('Ping daemon {}'.format(daemon_host))
        sock.sendto(cPickle.dumps('ping'), (host, int(port)))
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
    node = request.args['node']
    status = request.args.get('status', '')
    message = request.args.get('message', '')
    print('Emmit from {} message "{}"'.format(source, message))
    socketio.emit('update log', {'source': source, 'message': message, 'status': status, 'node': node})
    return Response(message)

@app.route('/get_file/<filename>')
def get_snapshot(filename):
    """Returns snapshot.jpg."""
    print "sending image: ", daemon_files, filename 
    print('{}/{}'.format(daemon_files, filename))
    return send_file('{}/{}'.format(daemon_files, filename), mimetype='image/jpeg')

@app.route('/finished/')
def finished():
    """Daemon finished. Emit signal to gui."""
    # The file is always in daemon_files directory
    filename = os.path.basename(request.args['filename'])
    print 'emit_finished', filename
    socketio.emit('finished', {'filename': '{}?t={}'.format(filename, time.time())})
    return Response('Ok')

@app.route('/partial/')
def partial():
    """Shown partial image."""
    filename = os.path.basename(request.args['filename'])
    print('emit partial', filename)
    socketio.emit('partial', {'filename': '{}?t={}'.format(filename, time.time())})
    return Response('OK')

@app.route('/pong/')
def pong():
    socketio.emit('daemon pong')
    return Response('OK')

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--host', default='0.0.0.0')
    args.add_argument('--port', default=5050, type=int)
    args.add_argument('--daemon_host', required=True, help='Path to daemon/hostname file')
    args.add_argument('--daemon_files', required=True, help='Path where daemon stores jpegs')
    args.add_argument('--camera_hostname', help='Camera hostname',
                      default='superpi.cs.kuleuven.be:8080')

    argv = args.parse_args()

    camera_hostname = argv.camera_hostname

    daemon_host = open(argv.daemon_host).read().strip()
    print('Daemon host: {}'.format(daemon_host))

    daemon_files = argv.daemon_files

    from socketio.server import SocketIOServer
    SocketIOServer((argv.host,argv.port), app, resource='socket.io', policy_server=False).serve_forever()

