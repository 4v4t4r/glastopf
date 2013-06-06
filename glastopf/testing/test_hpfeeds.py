# Copyright (C) 2013 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import unittest
import os
import tempfile
import shutil

import helpers
import glastopf.modules.events.attack as attack
from glastopf.modules.reporting.auxiliary.log_hpfeeds import HPFeedsLogger
from glastopf.modules.HTTP.handler import HTTPHandler

class Test_Loggers(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.files_dir = os.path.join(self.tmpdir, 'files')
        os.mkdir(self.files_dir)

    def tearDown(self):
        if os.path.isdir(self.tmpdir):
            shutil.rmtree(self.tmpdir)

    def test_hpfeeds_event(self):
        """Objective: Testing if a basic event can be transmitted using hpfriends."""

        config_file = tempfile.mkstemp()[1]
        with open(config_file, 'w') as f:
            f.writelines(helpers.gen_config(''))

        logger = HPFeedsLogger(self.tmpdir, config=config_file, reconnect=False)
        event = attack.AttackEvent()
        event.http_request = HTTPHandler('', None)
        event.raw_request = "GET /honeypot_test HTTP/1.1\r\nHost: honeypot\r\n\r\n"
        logger.insert(event)
        error_message = logger.hpc.wait(2)
        self.assertIsNone(error_message)

    def test_hpfeeds_event_with_file(self):
        """Objective: Testing if a event containing a file can be transmitted using hpfriends."""

        config_file = tempfile.mkstemp()[1]
        with open(config_file, 'w') as f:
            f.writelines(helpers.gen_config(''))

        #create dummy file
        file_name = 'dummy_file'
        with open(os.path.join(self.files_dir, file_name), 'w') as f:
            print self.files_dir
            f.write('test_test_test_test_test')

        logger = HPFeedsLogger(self.tmpdir, config=config_file, reconnect=False)
        event = attack.AttackEvent()
        event.http_request = HTTPHandler('', None)
        event.raw_request = "GET /honeypot_test HTTP/1.1\r\nHost: honeypot\r\n\r\n"
        event.file_name = file_name
        logger.insert(event)
        error_message = logger.hpc.wait(2)
        self.assertIsNone(error_message)
