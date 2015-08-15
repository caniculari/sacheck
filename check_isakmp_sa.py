#!/usr/bin/python3

# Nagios/Icinga plugin to validate isakmp sa to a particular host

import argparse
import pexpect

# Uses argparse to get the parameters for the plugin.
parser = argparse.ArgumentParser(
    prog = "check_cisco_isa_sa.py",
    description = "Check if a IPSec VPN is up in Cisco IOS")
parser.add_argument('-H', '--HOSTNAME', 
    required = True,
    help = 'Hostname or IP Address.')
parser.add_argument('-p', '--password',
    help = 'Access password. If your password has special characters put in quotes.')
parser.add_argument('-e', '--enable',
    help = 'Enable password.')
parser.add_argument('-c', '--connection',
    choices = ['telnet', 'ssh'],
    help = 'Connection type [ssh|telnet].')
parser.add_argument('-P', '--peer',
    required = True,
    help = 'VPN peer IP address.')
parser.add_argument('-u', '--user',
    required = True,
    help = 'username to login.')
parser.add_argument('-w', '--warning',
    help='Warning response.')

args = parser.parse_args()

hostname = args.HOSTNAME
password = args.password
enable = args.enable
conn = args.connection
peer = args.peer
user = args.user
warning = args.warning

#connection via ssh
def sshConnection():
    try:
        child = pexpect.spawn('ssh %s@%s' % (user, hostname))
        child.timeout = 4
        child.expect('[P,p]assword:')
        print ('exito hasta el ssh')
    except (pexpect.EOF, pexpect.TIMEOUT):
        print ("Can't connect")
        raise SystemExit

def telnetConnection():
    try:
        child = pexpect.spawn('ssh %s@%s' % (user, hostname))
        child.timeout = 4
        child.expect('[U,u]sername:')
        print('exito con telnet')
    except (pexpect.EOF, pexpect.TIMEOUT): 
        print ("Can't connect")
        raise SystemExit  

if (conn == "ssh"):
    sshConnection()

