#! /usr/bin/env python
#
# Copyright (c) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

from mpi4py import MPI
import time

import plogger

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

logger = plogger.PLogger(rank)


def process():
    logger.write('Hi I am doing something', status=3)
    time.sleep(5)
    logger.write('Ok I am done', status=2)
    comm.Barrier()
