import socket, pickle
import sys
import time
from random import randint
from udp_custom import udp_custom
from random import uniform
from socket_client import socket_client

server_address = ('localhost', 10000)
sock = socket_client()

data = udp_custom(syn=1, seq=randint(0,10000), ack=1)

try:
    sent = sock.sendto(data, server_address)
    data, server = sock.recvfrom()
    if data.syn == 1:
        data.syn = 0
        while data.fin != 1: 
            time.sleep(uniform(0.1, 2))   
            p = randint(0, 10)
            if p < 4:
                print('missed')
                continue
            sock.confirm_ack(data, server_address)
            data, server = sock.recvfrom()
 
finally:    
    print('closing socket')
    sock.close()

