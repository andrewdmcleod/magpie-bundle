#!/usr/bin/env python3

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import unittest

import yaml
import amulet


class TestBundle(unittest.TestCase):
    bundle_file = os.path.join(os.path.dirname(__file__), '..', 'bundle.yaml')

    @classmethod
    def setUpClass(cls):
        # classmethod inheritance doesn't work quite right with
        # setUpClass / tearDownClass, so subclasses have to manually call this
        cls.d = amulet.Deployment(series='xenial')
        with open(cls.bundle_file) as f:
            bun = f.read()
        bundle = yaml.safe_load(bun)
        cls.d.load(bundle)
        cls.d.setup(timeout=3600)
        cls.magpie_0 = cls.d.sentry['magpie'][0]
        cls.magpie_1 = cls.d.sentry['magpie'][1]
        cls.magpie_2 = cls.d.sentry['magpie'][2]
        cls.magpie_3 = cls.d.sentry['magpie'][3]
        cls.magpie_4 = cls.d.sentry['magpie'][4]
        cls.magpie_5 = cls.d.sentry['magpie'][5]
        cls.d.sentry.wait_for_messages({'magpie': 'icmp: ok, dns: ok'}, timeout=3600)

    def test_components(self):
        """
        Do nothing...
        """

    def break_dns_single(self):
        """Break DNS on one unit, make sure DNS check fails, fix DNS, toggle back"""
        self.magpie_0.run("sudo mv /etc/resolv.conf /etc/resolv.conf.bak")
        self.d.sentry.wait_for_messages({'magpie': ['icmp: ok', 'dns failed']}, timeout=3600)
        self.magpie_0.run("sudo mv /etc/resolv.conf.bak /etc/resolv.conf")
        self.d.sentry.wait_for_messages({'magpie': 'icmp: ok, dns ok'}, timeout=3600)

    def break_dns_all(self):
        """Set DNS with action to 255.255.255.255 - All units should fail DNS."""
        self.d.configure('magpie', {'dns_server': '255.255.255.255'}, timeout=3600)
        self.d.sentry.wait_for_messages({'magpie': re.compile('icmp: ok, dns failed')})
        self.d.configure('magpie', {'dns_server': ''}, timeout=3600)
        self.d.sentry.wait_for_messages({'magpie': 'icmp: ok, dns ok'})

    def break_ping_single(self):
        """Take primary interface down and make sure ICMP fails."""
        interface, retcode = self.magpie_1.run("ip route get 255.255.255.255")
        interface = interface.split(" ")[3]
        self.magpie_1("sudo ifconfig {} down".format(interface))
        self.d.sentry.wait_for_messages({'magpie': re.compile('icmp: failed, dns failed')})

if __name__ == '__main__':
    unittest.main()
