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
        query_result = (login(child))
        query_result = query_result.decode(encoding='utf-8')
        child.close()
        return query_result
    except (pexpect.EOF, pexpect.TIMEOUT):
        print ("Can't connect")
        raise SystemExit

def telnetConnection():
    try:
        child = pexpect.spawn('ssh %s@%s' % (user, hostname))
        child.timeout = 4
        login(child)
    except (pexpect.EOF, pexpect.TIMEOUT): 
        print ("Can't connect")
        raise SystemExit  

def login(child):
    child.expect('[P,p]assword:')
    child.sendline(password)
    child.expect('\n*#')
    child.sendline("show crypto isakmp sa")
    child.expect('\n*#')
    return (child.before)


if (conn == "ssh"):
    vpn_status = sshConnection()
    #vpn_status = vpn_status[vpn_status.find(peer):vpn_status.find("QM_IDLE")+7]
    #vpn_status = vpn_status[vpn_status.find('src'):vpn_status.find("\r\n")]
    print (vpn_status)
    print (repr(vpn_status)) 
