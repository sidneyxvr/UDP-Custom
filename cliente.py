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
start_time = time.time()
c = 0
try:
    sent = sock.sendto(data, server_address)
    
    data, server = sock.recvfrom()
    
    if data.syn == 1:
        data.ack += 1
        data.syn = 0
        sock.sendto(data, server)
        print('fin',data.fin)
        while data.fin != 1: 
            data.syn = 0
            time.sleep(uniform(0.1, 0.5))   
            c += 1
            p = randint(0, 9)
            data, server = sock.recvfrom()
            print('recebido',data.seq)
            if p < 1: #10%
                print('perdido', data.seq)
            else:
                sock.confirm_ack(data, server_address)
        sock.close_server_connection(server_address)
            
finally:    
    end_time = time.time()
    print('tempo total', (end_time - start_time))
    print('tempo médio de espera','{:.4f}'.format((end_time - start_time)/c),'s')
    sock.close()

