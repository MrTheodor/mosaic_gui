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

execfile('params.par')

logger = plogger.PLogger(rank, host_url=LOGGER_HOST)


def process():
    logger.write('Hi I am ready', status=plogger.IDLE)
    for s in plogger.valid_status:
        time.sleep(s+1)
        logger.write('Ok - {}'.format(s), status=s)
    comm.Barrier()
