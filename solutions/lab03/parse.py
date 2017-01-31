#############################################
#  Create a script, that will connect to    #
#  router (using ssh) and execute           #
#  "show ip interface brief" command. Then  #
#  parse the output for IP addresses.       #
#  Create a dictionary of all interfaces    #
#  with IP address. Use interface as key    #
#  and IP address as value.                 #
#############################################

import paramiko
import time
import re

host = '192.168.35.121'
username = 'cisco'
password = 'cisco'


# Send command and read the output
# @param shell - Shell objcet
# @param command - Command to execute
def sendCommand(shell, command):
    shell.send(command + '\n')
    time.sleep(1)
    if shell.recv_ready():
        data = shell.recv(65535)
    return data


def getIpInterfaceBrief():
    client = paramiko.SSHClient()
    policy = paramiko.client.WarningPolicy()
    client.set_missing_host_key_policy(policy)
    client.connect(host, username=username, password=password)
    shell = client.invoke_shell()
    sendCommand(shell, 'terminal length 0')
    ipIntBriefOutput = sendCommand(shell, 'show ip interface brief')
    client.close()
    return ipIntBriefOutput


# Create empty dictionary
interfaceDict = dict()
# Execture the command and get the outpt
output = getIpInterfaceBrief()
# Iterate through all lines
for line in output.splitlines():
    # Search for IP address in line
    searchIP = re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', line)
    # If searchIP is not Nont, then get the interface and IP address
    if searchIP:
        interfaceDict[line.split(' ')[0]] = searchIP.group(0)
print interfaceDict
