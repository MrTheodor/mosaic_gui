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
qsub run_job.pbs

echo "Starting web..."
cd ..
cd web
nohup python test_server.py --daemon_host ../daemon/hostname --daemon_files ../daemon/files &
cd ..

echo "Let's play..."
