import socket, pickle
import sys
import time
from udp_custom import udp_custom
from socket_custom import socket_custom
from timeout import timeout


# Create a UDP socket
server_address = ('localhost', 10000)
sock = socket_custom()
sock.bind(server_address)

while True:
    data, address = sock.recvfrom()
    if data.syn == 1: #establishing connection
        sock.confirm_connetion(data, address)
    else: #stablished connection
        sock.send_packet(data, address)
        