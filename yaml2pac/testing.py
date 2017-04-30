#!/usr/bin/env python
# coding: utf-8

import sys
import time
import random
import logging
import traceback
import multiprocessing
import SocketServer
import SimpleHTTPServer

from yaml2pac.core import RULE_TYPES
from yaml2pac.utils import cidr_iprange, call_cmd


def generate_urls(pac_args):
    """
    The returning `urls` contains three rule type copied from `pac_args`,
    the difference is that `keyword` and `ip` are converted into valid urls
    so that they could be a real example of what they previously indicate:
    {
        'domain': {
            'a.com': 1,
            'c.com': 'https_1',
        },
        'keywords': {
            'b.com': 1,
            'd.com': 'https_1',
        },
        'ip': {
            '8.8.1.2': 1,
            '114.114.114.3': 'https_1'
        }
    }
    """
    urls = {}
    for i in RULE_TYPES:
        if i not in pac_args:
            continue
        rules = pac_args[i]
        sub_urls = {}
        if i == 'domain':
            sub_urls = dict(rules)
        elif i == 'keyword':
            for k, v in rules.iteritems():
                url = '{}.com'.format(k)
                sub_urls[url] = v
        else:  # i == 'ip'
            for k, v in rules.iteritems():
                ips = list(cidr_iprange(k))
                random_ip = ips[random.randint(0, len(ips) - 1)]
                sub_urls[random_ip] = v
        urls[i] = sub_urls
    return urls


class ReusableTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True


def start_proxy_server(name, port):

    class ProxyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):  # NOQA
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(name)

    server = ReusableTCPServer(("", port), ProxyHandler)

    logging.info("Start proxy server: %s %s", name, port)
    server.serve_forever()


def start_pac_server(pac_text, port):

    class PACHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def do_GET(self):  # NOQA
            self.send_response(200)
            self.send_header('Content-Type', 'application/x-ns-proxy-autoconfig')
            self.end_headers()
            self.wfile.write(pac_text)

    server = ReusableTCPServer(("", port), PACHandler)

    logging.info("Start pac server: %s", port)
    server.serve_forever()


def osx_set_system_proxy_pac(pac_url):
    services, rc = call_cmd(['networksetup', '-listallnetworkservices'])
    services = services[1:]
    print ('Select which network service are you using, '
           'usually its Wi-Fi or Ethernet')
    for loop, service in enumerate(services):
        if service:
            print '{}) {}'.format(loop + 1, service)
    chosen = raw_input()
    service = services[int(chosen) - 1]
    _, rc = call_cmd(['sudo', 'networksetup', '-setautoproxyurl',
                      service, pac_url])
    if rc != 0:
        print 'set system proxy failed:', _, rc
        raise RuntimeError()


def start_testing(pac_args, pacfile, requester, proxy_port=34000, pac_port=35000):
    # Determine which system proxy function to use by OS
    if sys.platform == 'darwin':
        set_system_proxy_pac = osx_set_system_proxy_pac
    else:
        raise NotImplementedError('Currently only support on OS X now')

    # Preparations
    with open(pacfile, 'r') as f:
        pac_text = f.read()
    pac_url = 'http://127.0.0.1:{}/proxy.pac'.format(pac_port)

    proxies = pac_args['proxies']
    dummy_proxies = {}
    for k, v in proxies.iteritems():
        dummy_proxies[k] = proxy_port
        proxy_port += 1

    # Replace proxy in pac text
    for proxy_name, proxy_value in proxies.iteritems():
        dummy_proxy_value = 'PROXY 127.0.0.1:{}'.format(dummy_proxies[proxy_name])
        pac_text = pac_text.replace(proxy_value, dummy_proxy_value)

    # Start proxy servers
    server_processes = []
    for k, v in dummy_proxies.iteritems():
        server_process = multiprocessing.Process(target=start_proxy_server, args=(k, v))
        server_process.start()
        server_processes.append(server_process)

    # Define teardown function
    def stop_processes():
        # Terminate proxy servers
        for i in server_processes:
            logging.info('Terminate server %s' % i._args[1])
            i.terminate()

    # Start pac server
    pac_server_process = multiprocessing.Process(
            target=start_pac_server, args=(pac_text, pac_port))
    pac_server_process.start()
    server_processes.append(pac_server_process)

    # Set system proxy to pac url
    set_system_proxy_pac(pac_url)

    # Generate urls for test
    try:
        urls = generate_urls(pac_args)
        print urls
    except Exception as e:
        traceback.print_exc()
        stop_processes()
        return

    time.sleep(20)

    stop_processes()
