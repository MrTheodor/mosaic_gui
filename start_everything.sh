#! /bin/sh
#
# start_everything.sh
# Copyright (C) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

echo "Staring stream server..."
nohup ./start_stream.sh &

echo "Starting daemon..."
cd daemon
rm -f hostname

qsub run_job.pbs

until [ -f hostname ]
do
     sleep 2
done

echo "Starting web..."
cd ..
cd web
nohup python test_server.py --daemon_host /home/pi/mosaic_gui/daemon/hostname --daemon_files /home/pi/mosaic_gui/daemon/output &
cd ..

echo "Let's play..."
