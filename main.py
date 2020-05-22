#!/usr/bin/python

import sys
import getopt
import requests
import json

from binascii import a2b_hex
from hashlib import sha1

options, remainder = getopt.getopt(sys.argv[1:], 'f:sih', ['fingerprint=', 
                                                        'info',
                                                        'help',
                                                        'hashed-fingerprint'
                                                        ])
fingerprint = False
hashed_fingerprint = False
show_info = False

for opt, arg in options:
    if opt in ('-f', '--fingerprint'):
        fingerprint = arg
    elif opt in ('-i', '--info'):
        show_info = True
    elif opt in ('-s', '--hashed-fingerprint'):
        hashed_fingerprint = True
    elif opt in ('-h', '--help'):
        print("Usage:\n %s [-i] -f <fingerprint>\n\nOptions:\n -f, --fingerprint=<fingerprint>\tGet status of a tor bridge (0: online, 1: offline, 2: not exists) [REQUIRED PARAM]\n\t\t\t\t\t Fingerprint must not be hashed\n -s, --hashed-fingerprint\t\tSearch for hashed fingerprint\n -i, --info\t\t\t\tGet info from bridge only if it is online\n -h, --help\t\t\t\tshow this help\n" % sys.argv[0])
        quit()

if not fingerprint:
    print("Usage: ./%s -f <fingerprint>\nCheck '%s --help' for more info" % (sys.argv[0], sys.argv[0]) )
    quit()

if not hashed_fingerprint:
    try:
        fingerprint = sha1(a2b_hex(fingerprint)).hexdigest()
    except:
        print("[X] Fingerprint format error")
        quit()

url = 'https://onionoo.torproject.org/details?lookup=%s' % fingerprint

r = requests.get(url)
data = json.loads(r.text)
#print(data)

if len(data['bridges']):
    b = data['bridges'][0]
    if b['running']:
        print(0) # ONLINE
    else:
        print(1) # OFFLINE

else:
    print(3) # NOT EXIST
