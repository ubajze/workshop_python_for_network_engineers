##################################################
#  Create a script, that will use the Jinja2     #
#  template, to generate 10 loopback interfaces  #
#  with IP addresses from 172.16.0.1/32 to       #
#  172.16.9.1/32.                                #
##################################################

import jinja2
import paramiko
import time

server = '192.168.35.130'
host = '192.168.35.121'
username = 'cisco'
password = 'cisco'


# Method to load the template
def load_template():
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

    return template


def create_loopbacks(count=10):
    loopback_dictionary = dict()
    for i in range(count):
        loopback_dictionary['loopback 100{}'.format(str(i))] = '172.16.{}.1'.format(str(i))
    return loopback_dictionary


# Send command and read the output
# @param shell - Shell objcet
# @param command - Command to execute
def send_command(shell, command):
    shell.send(command + '\n')
    time.sleep(1)
    if shell.recv_ready():
        data = shell.recv(65535)
    return data


def create_connection():
    # Create the paramiko SSH instance
    client = paramiko.SSHClient()
    policy = paramiko.client.WarningPolicy()
    client.set_missing_host_key_policy(policy)
    # Connect to the host and invoke shell
    client.connect(host, username=username, password=password)
    # You need to invoke shell to open interactive shell for multiple commands
    return client


def close_connection(connection):
    connection.close()


if __name__ == '__main__':

    # Get the loopback interface disctionary
    loopback_dictionary = dict()
    loopback_dictionary['interfaces'] = create_loopbacks()

    # Load the template
    template = load_template()

    # Render the template
    template_rendered = template.render(loopback_dictionary)

    # Save template to file
    f = open('/var/www/html/config.txt', 'w')
    f.write(template_rendered)
    f.close()

    # Create connection
    client = create_connection()
    shell = client.invoke_shell()

    # Copy file from HTTP server to router
    command = "copy http://{}/config.txt bootflash".format(server)
    send_command(shell, command)


