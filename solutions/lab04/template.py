##################################################
#  Create a script, that will use the Jinja2     #
#  template, to generate 10 loopback interfaces  #
#  with IP addresses from 172.16.0.1/32 to       #
#  172.16.9.1/32.                                #
##################################################

import jinja2
import paramiko
import time
import ipaddr

server = '192.168.35.130'
host = '192.168.35.121'
username = 'cisco'
password = 'cisco'
super_class = '172.16.0.0/16'
loopback_count = 10


##############################################################################
# Create the method that load the template and returns the
# Jinja2 template object
##############################################################################
def load_template():
    # Create loader to search for templates in current folder
    loader = jinja2.FileSystemLoader('.')
    # Establish environment
    env = jinja2.Environment(loader=loader)
    # Load the template
    template = env.get_template('interface.template')

    # # Alternatively, you can read the file and use the jinja2.Template class
    # # Open and read file
    # f = open('interface.template', 'r')
    # template_data = f.read()
    # f.close()
    # # Load the template
    # template = jinja2.Template(template_data)

    return template
##############################################################################


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


##############################################################################
# Create the method that accepts the super_class and number of interfaces
# and calculates the as many /30 subnets as specified in the argument. It
# should start with first available subnet.
##############################################################################
def calculate_ip_addresses(super_class, loopback_count):
    loopback_dictionary = dict()

    ip_network = ipaddr.IPv4Network(super_class)
    current_ip = ipaddr.IPv4Network(str(ip_network.ip + 1) + '/30')
    loopback_dictionary[1000] = str(current_ip.ip)
    for i in range(1, loopback_count):
        current_ip = ipaddr.IPv4Network(str(current_ip.ip + 4) + '/30')
        loopback_dictionary[1000 + i] = str(current_ip.ip)
    return loopback_dictionary
##############################################################################


def main():

    ##############################################################################
    # Create a dictionary with Loopback ID as key and IP address as value
    ##############################################################################
    loopback_dictionary = calculate_ip_addresses(super_class, loopback_count)
    ##############################################################################


    ##############################################################################
    # Load the template
    ##############################################################################
    template = load_template()
    ##############################################################################


    ##############################################################################
    # Render the template
    ##############################################################################
    template_rendered = template.render(loopback_dictionary)
    ##############################################################################


    ##############################################################################
    # Save template to file at the location /var/www/html/config.txt
    ##############################################################################
    f = open('/var/www/html/config.txt', 'w')
    f.write(template_rendered)
    f.close()
    ##############################################################################


    ##############################################################################
    # Establish the connection with the router
    # Copy the config file from the server to the router
    # Copy config file from the bootflash to the running-config
    ##############################################################################
    client = init_connection()
    shell = client.invoke_shell()

    # Copy file from HTTP server to router
    command = "copy http://{}/config.txt bootflash".format(server)
    print send_command(shell, command)
    print send_command(shell, '')
    print send_command(shell, '')   # Two \n are needed if config.txt already exists on the router

    # Copy configuration to the running-configuration
    command = "copy bootflash:config.txt system:running-config"
    print send_command(shell, command)
    print send_command(shell, '')
    ##############################################################################


    ##############################################################################
    # Verify the status of the interfaces with "show ip interface brief"
    ##############################################################################
    send_command(shell, 'terminal length 0')
    output = send_command(shell, 'show ip interface brief')
    print output
    ##############################################################################


    ##############################################################################
    # CLose the connection
    ##############################################################################
    client.close()
    ##############################################################################


if __name__ == "__main__":
    main()
