#! /bin/sh
#
# start_stream.sh
# Copyright (C) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

killall -9 -f mjpg_streamer

PATH_TO_MJPG="mjpg-streamer/mjpg-streamer-experimental"

# Place where snapshots will be saved. It has to be an absolute path!
OUTPUT_FILES="daemon/output"

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$PATH_TO_MJPG"

# Webcam
#$PATH_TO_MJPG/mjpg_streamer -i "input_uvc.so" -o "output_http.so" -o "output_file.so -f $OUTPUT_FILES --http"
# Rasbian
#$PATH_TO_MJPG/mjpg_streamer -i "input_raspicam.so -hf -vf -quality 100 " -o "output_http.so" -o "output_file.so -f $OUTPUT_FILES --http"
$PATH_TO_MJPG/mjpg_streamer -i "input_raspicam.so -hf -vf -quality 100 -y 1280 -x 720 -rot 90" -o "output_http.so" -o "output_file.so -f $OUTPUT_FILES --http"
