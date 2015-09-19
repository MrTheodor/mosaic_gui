#! /usr/bin/env python
# vim:fenc=utf-8
#
# Copyright (C) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#                    Keith Myerscough
#                    Korneel Dumon
#
# Distributed under terms of the GNU GPLv2 license.
#
# Idea fix:
# Daemon will wait for message on port 9090. The message will contain
# path to source image, search term and recipient e-mail address.
#
# Currently it can only handle single client.
#


import cPickle
import SocketServer
import socket
from mpi4py import MPI

import plogger
import node
import master

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

logger = plogger.PLogger(rank)

class UDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = cPickle.loads(self.request[0])
        print('{} wrote: {}'.format(self.client_address[0], data))
        master.process(data)

if rank == 0:
    # Running UDP server in infinite loop on master node. Waiting for connection
    # from client.
    hostname = socket.gethostname()
    port = 9090
    with open('hostname', 'w') as f:
        f.write('{}:{}'.format(hostname, port))
    logger.write('{} starting listening server on {}:{}'.format(rank, hostname, port))
    server = SocketServer.UDPServer((hostname, 9090), UDPHandler)
    server.serve_forever()
else:
    # Infinite loop. Waiting for signal from rank=0 to start node.process().
    while True:
        signal = None
        comm.bcast(signal, root=0)
        node.process()
