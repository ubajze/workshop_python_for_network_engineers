##################################################
#  Create a script, that will use the Jinja2     #
#  template, to generate 10 loopback interfaces  #
#  with IP addresses from 172.16.0.1/32 to       #
#  172.16.9.1/32.                                #
##################################################

import jinja2
import paramiko
import time

host = '192.168.35.121'
username = 'cisco'
password = 'cisco'

# Load the jinja2 template
# Create loader to search for templates in current folder
loader = jinja2.FileSystemLoader('.')
# Establish environment
env = jinja2.Environment(loader=loader)
# Load template
template = env.get_template('interface.template')

# # Alternativly, you can read the file and use the jinja2.Template class
# # Open and read file
# f = open('interface.template', 'r')
# template_data = f.read()
# f.close()
# # Load template
# template = jinja2.Template(template_data)


def createLoopbackDict(count=10):
    loopDict = dict()
    for i in range(count):
        loopDict['loopback 100{}'.format(str(i))] = '172.16.{}.1'.format(str(i))
    return loopDict


# Send command and read the output
# @param shell - Shell objcet
# @param command - Command to execute
def sendCommand(shell, command):
    shell.send(command + '\n')
    time.sleep(1)
    if shell.recv_ready():
        data = shell.recv(65535)
    return data


def create_shell():
    # Create the paramiko SSH instance
    client = paramiko.SSHClient()
    policy = paramiko.client.WarningPolicy()
    client.set_missing_host_key_policy(policy)
    # Connect to the host and invoke shell
    client.connect(host, username=username, password=password)
    # You need to invoke shell to open interactive shell for multiple commands
    shell = client.invoke_shell()
    return shell


loopDict = createLoopbackDict()
for line in template.render({'interfaces': loopDict}).splitlines():
    print repr(line)
