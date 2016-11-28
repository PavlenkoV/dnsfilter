#! /usr/bin/python2
# Based on demonstration example
# http://twistedmatrix.com/documents/current/names/howto/custom-server.html
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
# https://opensource.org/licenses/mit-license.php

import json
import io

from twisted.internet import reactor, defer
from twisted.names import client, dns, error, server


class DynamicResolver():

    def __init__(self, pattern, log_flag, log_flag_all):
        self._pattern = pattern
        self._log_flag = log_flag
        self._log_flag_all = log_flag_all

    def _dynamicResponseRequired(self, query):

        if self._log_flag_all.lower() == 'yes':
            with open("log_all", "a") as log_file:
                log_file.write('{}\n'.format(query.name.name))
        if query.type == dns.A or dns.AAAA:
            for domain_name in self._pattern:
                if domain_name in query.name.name:
                    return True
        return False

    def _doDynamicResponse(self, query):

        name = query.name.name
        if self._log_flag.lower() == 'yes':
            with open("log", "a") as log_file:
                log_file.write('{}\n'.format(name))
        answer = dns.RRHeader(
            name=name,
            payload=dns.Record_A(address=b'127.0.0.1'))
        answers = [answer]
        authority = []
        additional = []

        # print 'RRHeader - {}{}'.format((answers, authority, additional),
        # answer.payload)

        return answers, authority, additional

    def query(self, query, timeout=None):

        if self._dynamicResponseRequired(query):
            return defer.succeed(self._doDynamicResponse(query))
        else:
            return defer.fail(error.DomainError())


class InitialSetup():

    def openConf(self):
        with open('conf.json') as json_conf:
            config = json.load(json_conf)

            blacklist = config['blacklist']
            title = config['html_page']['title']
            text = config['html_page']['text']
            show_domains = config['html_page']['show_forbidden_domains']
            server1 = config['servers']['primary']
            server2 = config['servers']['secondary']
            log_flag = config['log_file_forbidden']
            log_flag_all = config['log_file_all']
        return title, text, show_domains, blacklist, server1, \
            server2, log_flag, log_flag_all

    def parsingIndexHTML(self, pattern):
        title, text, show_domains, blacklist = pattern

        with io.open('index.html', encoding='utf8') as f:
            data = []
            for line in f:
                if line.lstrip().startswith('<title>'):
                    nr_whitespaces = len(line) - len(line.lstrip())
                    line = ' ' * nr_whitespaces + '<title>' + title + \
                        '</title>\n'
                    data.append(line)
                elif line.lstrip().startswith('<h1>'):
                    nr_whitespaces = len(line) - len(line.lstrip())
                    line = ' ' * nr_whitespaces + '<h1>' + text + '</h1>\n'
                    data.append(line)
                elif line.lstrip().startswith("<p id='parser'>"):
                    nr_whitespaces = len(line) - len(line.lstrip())
                    if show_domains == 'yes':
                        line = ' ' * nr_whitespaces + "<p id='parser'>" + \
                            ', '.join(blacklist) + '</p>\n'
                        data.append(line)
                    else:
                        line = unicode(' ' * nr_whitespaces +
                                       "<p id='parser'>" + '</p>\n')
                        data.append(line)
                else:
                    data.append(line)

        with io.open('index.html', 'w', encoding='utf8') as f:
            f.writelines(data)


def main():
    """
    1) getting data from conf.json;
    2) updating Index.html;
    3) run dnsfilter server
    """
    openconf = InitialSetup().openConf()
    pattern = openconf[3]
    server1 = openconf[4]
    server2 = openconf[5]
    log_flag = openconf[6]
    log_flag_all = openconf[7]

    parser_data = openconf[0: 4]
    InitialSetup().parsingIndexHTML(parser_data)

    factory = server.DNSServerFactory(
        clients=[DynamicResolver(pattern, log_flag, log_flag_all),
                 client.Resolver(servers=[(server1, 53), (server2, 53)])]
    )

    protocol = dns.DNSDatagramProtocol(controller=factory)

    reactor.listenUDP(53, protocol)
    reactor.listenTCP(53, factory)

    reactor.run()


if __name__ == '__main__':
    raise SystemExit(main())
