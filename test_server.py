#! /usr/bin/env python
#
# Copyright (c) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

from flask import Flask, render_template, Response, request
from flask import stream_with_context
import cv2
import Image
import StringIO
from flask.ext.socketio import SocketIO, emit
import base64
from gevent.wsgi import WSGIServer
import requests

class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        ret, png = cv2.imencode('.png', image)
        return png.tostring()


app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)


def gen(cam):
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    n = request.args.get('n', 0)
    url = 'http://localhost:8080/?action=snapshot&n={}'.format(n)
    req = requests.get(url)
    return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])
    #return Response(gen(Camera()),
    #                mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/processing')
def processing():
    return render_template('processing.html')


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
    SocketIOServer(('0.0.0.0', 5050), app,
                   resource="socket.io", policy_server=False).serve_forever()
