#! /usr/bin/env python
#
# Copyright (c) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

from mpi4py import MPI
import os

import plogger

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

SNAPSHOT = "/home/teodor/project/mosaic_web/daemon/files/snapshot.jpg"

logger = plogger.PLogger(rank)

def process(data):
    print 'Hi I am master, rank ', rank
    print 'I will notify other nodes to start processing'
    comm.bcast(None, root=0)
    logger.write('btw, I\'ve got some data {} cool!'.format(data))
    logger.write('search tag {}'.format(data['search']))
    logger.write('result send {}'.format(data['email']))
    if os.path.exists(SNAPSHOT):
        logger.write('found {}'.format(SNAPSHOT))
