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


##############################################################################
# Create the method that establishes the connection and returns
# the paramiko connection instance
##############################################################################
def init_connection():
    client = paramiko.SSHClient()
    policy = paramiko.client.WarningPolicy()
    client.set_missing_host_key_policy(policy)
    client.connect(host, username=username, password=password)
    return client
##############################################################################


##############################################################################
# Create the method that accepts the paramiko connection instance
# and close the connection
##############################################################################
def close_connection(client):
    client.close()
##############################################################################


def main():
    ##############################################################################
    # Establish connection using init_connection()
    # Invoke shell
    # Send command using send_command()
    # Close the connection
    ##############################################################################
    client = init_connection()
    shell = client.invoke_shell()
    send_command(shell, 'terminal monitor 0')
    output = send_command(shell, 'show ip interface brief')
    close_connection(client)
    ##############################################################################


    ##############################################################################
    # Iterate through lines in output and search for IP address in the line
    # Save the IP address and interface in dictionary in the format:
    # <interface>: <ip_address>
    ##############################################################################
    interface_dict = dict()
    for line in output.splitlines():
        # Search for IP address in line
        search_IP = re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', line)
        # If search_IP is not None, then get the interface and IP address
        if search_IP:
            interface_dict[line.split(' ')[0]] = search_IP.group(0)
    ##############################################################################


    ##############################################################################
    # Print the dictionary
    ##############################################################################
    print interface_dict
    ##############################################################################


if __name__ == "__main__":
    main()
