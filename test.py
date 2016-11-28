# -*- coding: utf-8 -*-
import unittest
import socket
import json


class NewTest(unittest.TestCase):

    def setUp(self):

        def openConf():
            with open('conf.json') as json_conf:
                config = json.load(json_conf)
                blacklist = config['blacklist']
            return blacklist

        self.blacklist = openConf()
        self.hostlist = [socket.gethostbyname(name) for name in self.blacklist]
        self.checklist = ['127.0.0.1' for x in range(len(self.hostlist))]
        print zip(self.blacklist, self.checklist)

    def test_it_worked(self):

        self.assertListEqual(
            self.hostlist, self.checklist)


if __name__ == '__main__':
    unittest.main()
