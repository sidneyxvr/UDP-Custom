import socket, pickle
import sys
import time
from udp_custom import udp_custom
from threading import Thread, Event

class socket_client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__address = ('', 0)
        self.__buffer = dict()

    def confirm_ack(self, data, server_address):
        #1000 = payload
        # data.ack = data.seq + 1000#len(data.payload)
        self.__buffer[data.seq + 1000] = 1000
        p = self.f()
        print('f',p)
        data.ack = p
        sent = self.sendto(data, server_address)
        
        print('send ack', data.ack)  

    def sendto(self, data, address):
        return self.sock.sendto(pickle.dumps(data), address)

    def recvfrom(self):
        data, server = self.sock.recvfrom(4096)
        return pickle.loads(data), server

    def close(self):
        self.sock.close()

    def f(self):
        j = 1
        k = (0, 0)
        print(sorted(self.__buffer))
        for i in sorted(self.__buffer):
            if j == 1:
                j += 1
                k = i, self.__buffer[i]
                continue
            if k[0] + k[1] + 10 < i:
                return k[0]
            k = i, self.__buffer[i]
        return k[0]
            
            
            