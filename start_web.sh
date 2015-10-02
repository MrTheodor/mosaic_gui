#! /bin/sh
#
# start_everything.sh
# Copyright (C) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#


echo "Starting web..."
cd web
nohup python test_server.py --daemon_host /home/pi/mosaic_gui/daemon/hostname --daemon_files /home/pi/mosaic_gui/daemon/output &
cd ..
