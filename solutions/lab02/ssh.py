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


##############################################################################
# Create the method that accept shell object instance and command
# The method should return the output
##############################################################################
def send_command(shell, command):
    shell.send(command + '\n')
    time.sleep(1)
    if shell.recv_ready():
        data = shell.recv(65535)
    return data
##############################################################################


def main():
    ##############################################################################
    # Create the paramiko SSH instance
    ##############################################################################
    client = paramiko.SSHClient()
    ##############################################################################


    ##############################################################################
    # Create a missing host key warning policy
    ##############################################################################
    policy = paramiko.client.WarningPolicy()
    client.set_missing_host_key_policy(policy)

    # It is better to load known_hosts from the system
    # using the following procedure
    # client.load_host_keys('~/.ssh/known_hosts')
    ##############################################################################


    ##############################################################################
    # Connect to the host and invoke shell
    ##############################################################################
    client.connect(host, username=username, password=password)
    # You need to invoke shell to open interactive shell for multiple commands
    shell = client.invoke_shell()
    ##############################################################################


    ##############################################################################
    # Send the command to the router
    ##############################################################################
    # Set the terminal lenght to 0
    send_command(shell, 'terminal length 0')
    output = send_command(shell, 'show ip interface brief')
    print output

    # This is alternative method to send single command
    #
    # stdin, stdout, stderr = client.exec_command('show ip interface brief')
    # print stdout.read()
    # print stderr.read()
    ##############################################################################


    ##############################################################################
    # Close the connection
    ##############################################################################
    client.close()
    ##############################################################################


if __name__ == "__main__":
    main()
