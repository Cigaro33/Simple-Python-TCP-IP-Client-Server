import socket
import sys
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.24', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    while True:
        message = raw_input(">")
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)
        data = sock.recv(255)
        print >>sys.stderr, 'received "%s"' % data


except KeyboardInterrupt:
    exit()
finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
