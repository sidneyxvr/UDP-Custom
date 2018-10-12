import socket, pickle
import sys
import time
from udp_custom import udp_custom
from socket_custom import socket_custom
from timeout import timeout
from threading import Thread, Semaphore, Condition
# from threading import Thread
server_address = ('localhost', 10000)
sock = socket_custom()
sock.bind(server_address)

t1 = Thread(target=sock.recvpack)
t1.start()
# t1 = Thread(target=sock.recvpack)
# t1.start()

# t2 = Thread(target=sock.sendpack)
# t2.start()

# sem = Semaphore()

# th1 = Thread(target=sock.check_timeout, args=(sem))
# th1.start()

# while True:
#     sock.recvpack()
    # data, address = sock.recvpack()
    # if data.syn == 1: #establishing connection
    #     print('sdas')
    #     sock.confirm_connetion(data, address)
    # else: #stablished connection
    #     sock.sendpack()
    # if data.fin == 1:
    #     print('fim')


