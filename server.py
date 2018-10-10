import socket, pickle
import sys
import time
from udp_custom import udp_custom
from socket_custom import socket_custom
from timeout import timeout
from threading import Thread, Semaphore
# from threading import Thread
server_address = ('localhost', 10000)
sock = socket_custom()
sock.bind(server_address)

# sem = Semaphore()

# th1 = Thread(target=sock.check_timeout, args=(sem))
# th1.start()

while True:
    data, address = sock.recvfrom()
    if data.syn == 1: #establishing connection
        sock.confirm_connetion(data, address)
    else: #stablished connection
        sock.send_packet(data, address)
        print(data.seq)
    if data.fin == 1:
        print('fim')


