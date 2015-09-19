#! /bin/sh
#
# start_stream.sh
# Copyright (C) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

PATH_TO_MJPG="/home/teodor/project/mosaic_mjpeg/mjpg-streamer/mjpg-streamer-experimental"

# Place where snapshots will be saved. It has to be an absolute path!
OUTPUT_FILES="/home/teodor/project/mosaic_web/daemon/files"

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$PATH_TO_MJPG"

$PATH_TO_MJPG/mjpg_streamer -i "input_uvc.so" -o "output_http.so" -o "output_file.so -f $OUTPUT_FILES --http"
