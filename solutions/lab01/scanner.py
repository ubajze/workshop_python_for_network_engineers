################################################
#  Create a script, that will iterate through  #
#  given port list, and print OPEN or CLOSED   #
#  for each port.                              #
################################################

import telnetlib
import socket

# Port range
low_port = 1
high_port = 1000
host = '192.168.35.121'

# Iterate through all ports and try to establish the connection
for port in range(low_port, high_port + 1):
    try:
        conn = telnetlib.Telnet(host, port)
        conn.close()
        print "PORT {}: OPEN".format(str(port))
    # Catch the connections that are refused
    except socket.error:
        print "PORT {}: CLOSED".format(str(port))
