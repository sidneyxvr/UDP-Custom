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
        self.__buffer[data.seq + len(data.payload)] = len(data.payload)
        p = self.last_contiguous_ack()
        udp = udp_custom(ack=p)
        sent = self.sendto(udp, server_address)
        print('ack', udp.ack)  

    def sendto(self, data, address):
        return self.sock.sendto(pickle.dumps(data), address)

    def recvfrom(self):
        data, server = self.sock.recvfrom(4096)
        return pickle.loads(data), server

    def close_server_connection(self, server_address):
        udp = udp_custom(fin=1)
        self.sendto(udp, server_address)

    def close(self):
        self.sock.close()

    def last_contiguous_ack(self):
        j = 1
        k = (0, 0)
        for i in sorted(self.__buffer):
            if j == 1:
                j += 1
                k = i, self.__buffer[i]
                continue
            if k[0] + k[1] + 10 < i:
                return k[0]
            k = i, self.__buffer[i]
        return k[0]
            