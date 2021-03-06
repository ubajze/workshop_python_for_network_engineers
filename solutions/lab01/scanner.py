################################################
#  Create a script, that will iterate through  #
#  given port list, and print OPEN or CLOSED   #
#  for each port. The port range should be     #
#  passed as the arguments to the script.      #
################################################

import telnetlib
import socket
import sys


host = '192.168.35.121'


def main():
    ##############################################################################
    # Get the ports from the arguments
    ##############################################################################
    ports = sys.argv[1:]
    # Sort the ports so that you have low and high port
    ports.sort()
    ##############################################################################


    ##############################################################################
    # Iterate through all ports and try to establish the connection
    ##############################################################################
    for port in range(int(ports[0]), int(ports[1]) + 1):
        try:
            # Establish the connection and close the connection
            conn = telnetlib.Telnet(host, port)
            conn.close()
            print "PORT {}: OPEN".format(str(port))
        # Catch the connections that are refused
        except socket.error:
            print "PORT {}: CLOSED".format(str(port))
    ##############################################################################


if __name__ == "__main__":
    main()
