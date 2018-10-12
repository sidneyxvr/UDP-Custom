import socket, pickle
import sys
import time
from random import randint
from udp_custom import udp_custom
from random import uniform
from socket_client import socket_client

server_address = ('localhost', 10000)
sock = socket_client()

data = udp_custom(syn=1, seq=randint(0, 10000), ack=1)

try:
    sent = sock.sendto(data, server_address)
    
    data, server = sock.recvfrom()
    data.ack += 1
    sock.sendto(data, server)
    
    if data.syn == 1:
        data.syn = 0
        print('fin',data.fin)
        while data.fin != 1: 
            time.sleep(uniform(0.1, 0.5))   
            p = randint(0, 10)
            data, server = sock.recvfrom()
            print('pack recv',data.seq)
            if p < 4:
                print('missed', data.seq)
            else:
                sock.confirm_ack(data, server_address)
            
 
finally:    
    print('closing socket')
    sock.close()

