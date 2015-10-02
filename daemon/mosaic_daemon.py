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

import sys
sys.path.append('../../mosaic/')

import plogger
#import node
import master
import placer
import scraper

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
status = MPI.Status()

logger = plogger.PLogger(rank)

NScrappers = 4
NPlacers = 10
NIters = 2

int_pars = {'NScrapers': NScrappers, 'NPlacers': NPlacers, 'iters': NIters, 'per_page': 60, 'MaxTilesVert': 20, 'fidelity': 9, 'poolSize': 40, 'UsedPenalty': 0, 'useDB' : False}
string_pars = {'savepath' : './imgs/'}

# update default parameters with given values
# for i in range(len(sys.argv[:])):
#     name = sys.argv[i]
#     if name in int_pars:
#         int_pars[name] = int(sys.argv[i+1])

pars = dict(int_pars.items() + string_pars.items())

class UDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global pars
        global comm
        data = cPickle.loads(self.request[0])
        print('{} wrote: {}'.format(self.client_address[0], data))
        comm.Barrier()
        master.process(pars, data)

assert size == 1+pars['NScrapers']+pars['NPlacers']   
if rank == 0:
    hostname = socket.gethostname()
    port = 9090
    with open('hostname', 'w') as f:
        f.write('{}:{}'.format(hostname, port))
    logger.write('{} starting listening server on {}:{}'.format(rank, hostname, port))
    server = SocketServer.UDPServer((hostname, 9090), UDPHandler)
    print "master: starting server"
    server.serve_forever()
elif rank < 1+pars['NScrapers']:
    while True:
        print "scraper waiting"
        comm.Barrier()
        scraper.process(pars)
elif rank < 1+pars['NScrapers']+pars['NPlacers']:
    while True:
        print "placer waiting"
        comm.Barrier()
        placer_obj = placer.MinDistPlacer(pars)
        placer_obj.process()
        del placer_obj
    

MPI.Finalize()
