import socket, pickle
import sys
import time
from random import randint
from udp_custom import udp_custom
from random import uniform
from socket_custom import socket_custom

server_address = ('localhost', 10000)
sock = socket_custom()

data = udp_custom(syn=1, seq=randint(0,10000), ack=1)

try:
    sent = sock.sendto(data, server_address)
    data, server = sock.recvfrom()
    if data.syn == 1:
        data.syn = 0
        while data.fin != 1: 
            time.sleep(uniform(0.1, 2))     
            sock.confirm_ack(data, server_address)
            data, server = sock.recvfrom()
 
finally:
    print('closing socket')
    sock.close()

