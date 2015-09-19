#! /usr/bin/env python
#
# Copyright (c) 2015 Jakub Krajniak <jkrajniak@gmail.com>
#
# Distributed under terms of the GNU GPLv3 license.
#

import urllib


class PLogger(object):
    def __init__(self, source_rank, initial_status=0, host_url='http://0.0.0.0:5050'):
        self.rank = source_rank
        self.status = 0
        self.update_url = '{}/update_log/?'.format(host_url)

    def write(self, message, status=None):
        if status is not None:
            self.status = status
        params = {'source': self.rank, 'message': message, 'status': self.status}
        update_url = self.update_url + urllib.urlencode(params)
        try:
            urllib.urlopen(update_url)
        except IOError:
            pass
        print('{}: {}'.format(self.rank, message))
