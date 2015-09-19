#! /usr/bin/env python
#
# Copyright (c) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

from mpi4py import MPI
import os
import shutil
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate

import plogger

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Load params from file.
SNAPSHOT = None
SMTP_SERVER = None
SEND_FROM = None
execfile('params.par')

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

    # Wait for other nodes to finish
    comm.Barrier()

    # Dummy, only for test, copy input file to output_<timestamp>.jpg
    # and send e-mail.
    basedir = os.path.dirname(SNAPSHOT)
    output_file = 'output_{}.jpg'.format(time.time())
    print('Copy {} -> {}'.format(SNAPSHOT, os.path.join(basedir, output_file)))
    shutil.copyfile(SNAPSHOT, os.path.join(basedir, output_file))
    print('Send email to {}'.format(data['email']))
    msg = MIMEMultipart(
        From=SEND_FROM,
        To=data['email'],
        Date=formatdate(localtime=True),
        Subject='opendag superpi mosaic'
        )
    with open(os.path.join(basedir, output_file), 'rb') as output_mosaic:
        msg.attach(
            MIMEApplication(
                output_mosaic.read(),
                Content_Disposition='attachment; filename="{}"'.format(output_file),
                Name=output_file
            ))
    smtp = smtplib.SMTP(SMTP_SERVER)
    smtp.sendmail(SEND_FROM, data['email'], msg.as_string())
    smtp.close()
    logger.emit_finished(output_file)
    logger.write('finished', status=plogger.FINISHED)
