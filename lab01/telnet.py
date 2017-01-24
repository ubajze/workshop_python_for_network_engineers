############
#
# Connect to the router and execute the command.
#
############

import telnetlib
import socket
import sys

host = '192.168.35.121'
username = 'cisco'
password = 'cisco'
command = 'show ip interface brief'

try:
    # Establish the connection
    conn = telnetlib.Telnet(host)
except socket.error:
    print "Unable to connect to the router."

# Read the output for the username request and enter password
output = conn.read_until('Username: ', 3)
if 'Username: ' in output:
    conn.write(username + '\n')
else:
    print 'Cannot find the "Username: " string.'
    conn.close()
    sys.exit()

# Read the output for the password request and enter password
output = conn.read_until('Password: ', 3)
if 'Password: ' in output:
    conn.write(password + '\n')
else:
    print 'Cannot find the "Password: " string.'
    conn.close()
    sys.exit()

# Read for hash prompt
output = conn.read_until('#', 3)
if '#' in output:
    conn.write(command + '\n')
    output = conn.read_until('#', 3)
    print output

# Close the connection
conn.close()
