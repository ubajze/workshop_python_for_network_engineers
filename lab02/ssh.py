############################################
#  Create a script, that will connect to   #
#  router (using ssh) and execute          #
#  "show ip interface brief" command.      #
############################################

import paramiko
import time

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


# Create the paramiko SSH instance
client = paramiko.SSHClient()

# Either create a warning policy or load known_hosts file
policy = paramiko.client.WarningPolicy()
client.set_missing_host_key_policy(policy)
# client.load_host_keys('~/.ssh/known_hosts')

# Connect to the host and invoke shell
client.connect(host, username=username, password=password)
# You need to invoke shell to open interactive shell for multiple commands
shell = client.invoke_shell()

# Set the terminal lenght to 0
sendCommand(shell, 'terminal length 0')
ipIntBriefOutput = sendCommand(shell, 'show ip interface brief')
print ipIntBriefOutput

# # This is alternative method to send single command
# stdin, stdout, stderr = client.exec_command('show ip interface brief')
# print stdout.read()
# print stderr.read()
