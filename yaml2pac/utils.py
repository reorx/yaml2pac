#!/usr/bin/env python
# coding: utf-8

import socket
import struct
import subprocess


def call_cmd(args, print_cmd=True):
    """
    Call cmd by arguments list and return output as list of lines and exit code
    :param args: list
    :return: tuple
    """
    print ' '.join(args)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.split('\n'), p.returncode


def ipaddr_to_binary(ipaddr):
    """
    A useful routine to convert a ipaddr string into a 32 bit long integer
    """
    # from Greg Jorgensens python mailing list message
    q = ipaddr.split('.')
    return reduce(lambda a, b: long(a) * 256 + long(b), q)


def binary_to_ipaddr(ipbinary):
    """
    Convert a 32-bit long integer into an ipaddr dotted-quad string
    """
    # This one is from Rikard Bosnjakovic
    return socket.inet_ntoa(struct.pack('!I', ipbinary))


def cidr_iprange(ipaddr, cidrmask=None):
    """
    Creates a generator that iterated through all of the IP addresses
    in a range given in CIDR notation
    """
    # Get all the binary one's
    if cidrmask is None:
        try:
            ipaddr, cidrmask = tuple(ipaddr.split('/'))
        except ValueError:
            raise ValueError('Not a valid cidr ip address: {}'.format(ipaddr))
    mask = (long(2) ** long(32 - long(cidrmask))) - 1

    b = ipaddr_to_binary(ipaddr)
    e = ipaddr_to_binary(ipaddr)
    b = long(b & ~mask)
    e = long(e | mask)

    while b <= e:
        yield binary_to_ipaddr(b)
        b += 1
