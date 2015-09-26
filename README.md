Mosaic GUI
=========================

Setup
-------------------------

1. Clone repository

    The repositiory contains submodule so you have to clone it with `--recursive` option
    `git clone --recursive https://github.com/MrTheodor/mosaic_gui.git`

2. Update paths

    Edit file `daemon/params.par` and adjust paths.

    - `SNAPSHOT` path to snapshot file with the name at the end, it has to be `snapshot.jpg`.

    - `SMTP_SERVER` host name of SMTP SERVER

    - `SEND_FROM` e-mail address used to send e-mails

    - `LOGGER_HOST` HTTP URI that point to the web server
        e.g. `http://superpi.cs.kuleuven.be:5050/`


Components
-----------------------

- flask (http://flask.pocoo.org/)
- flask-socketio (https://flask-socketio.readthedocs.org/en/latest/)
- socketio (http://socket.io/)
- mjpg-streamer (https://github.com/jacksonliam/mjpg-streamer), fork in submodule
- Twitter bootstrap (http://getbootstrap.com/)
