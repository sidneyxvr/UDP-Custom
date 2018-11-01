import socket, pickle
import sys
import time
from udp_custom import udp_custom
from socket_server import socket_server

server_address = ('localhost', 10000)
sock = socket_server()
sock.bind(server_address)

sock.recvpack()
