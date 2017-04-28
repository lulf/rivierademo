#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import print_function, unicode_literals
import optparse
import random
import sys

from proton import Message
from proton.handlers import MessagingHandler
from time import sleep
from proton.reactor import Container
from datetime import datetime, timedelta

class Send(MessagingHandler):
    def __init__(self, url, messages, period):
        super(Send, self).__init__()
        self.url = url
        self.sent = 0
        self.confirmed = 0
        self.total = messages
        self.messages = messages
        self.period = period
        self.sender = None
        self.container = None

    def set_container(self, container):
        self.container = container

    def on_start(self, event):
        self.sender = event.container.create_sender(self.url)
        self.container.schedule(self.period, self)

    def on_timer_task(self, event):
        if self.sender and self.sender.credit:
            msg = Message(id=(self.sent+1), body={'sequence':(self.sent+1)})
            self.sender.send(msg)
            self.sent += 1
            if self.messages == 0:
                self.total = self.sent + 1
            # print (".", end="")
            sys.stdout.flush()
        self.container.schedule(self.period, self)

    def on_accepted(self, event):
        self.confirmed += 1

    def on_disconnected(self, event):
        self.sent = self.confirmed

parser = optparse.OptionParser(usage="usage: %prog [options]",
                               description="Send messages to the supplied address.")
parser.add_option("-a", "--address", default="localhost:5672/examples",
                  help="address to which messages are sent (default %default)")
parser.add_option("-m", "--messages", type="int", default=100,
                  help="number of messages to send (default %default)")
opts, args = parser.parse_args()

try:
    sender = Send(opts.address, opts.messages, random.uniform(0.03, 0.1))
    c = Container(sender)
    sender.set_container(c)
    c.run()
except KeyboardInterrupt: pass
