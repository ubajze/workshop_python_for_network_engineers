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

host = ''
username = ''
password = ''


##############################################################################
# Create the method that accept shell object instance and command
# The method should return the output
##############################################################################
def send_command(shell, command):

    return data
##############################################################################


##############################################################################
# Create the method that establishes the connection and returns
# the paramiko connection instance
##############################################################################
def init_connection():

    return client
##############################################################################


##############################################################################
# Create the method that accepts the paramiko connection instance
# and close the connection
##############################################################################
def close_connection(client):

##############################################################################


def main():
    ##############################################################################
    # Establish connection using init_connection()
    # Invoke shell
    # Send command using send_command()
    # Close the connection
    ##############################################################################

    ##############################################################################


    ##############################################################################
    # Iterate through lines in output and search for IP address in the line
    # Save the IP address and interface in dictionary in the format:
    # <interface>: <ip_address>
    ##############################################################################
    interface_dict = dict()

    ##############################################################################


    ##############################################################################
    # Print the dictionary
    ##############################################################################
    print interface_dict
    ##############################################################################


if __name__ == "__main__":
    main()
