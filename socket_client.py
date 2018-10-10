import socket, pickle
import sys
import time
from udp_custom import udp_custom

class socket_client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__address = ('', 0)

    def confirm_ack(self, data, server_address):
        data.ack = data.seq + 1000#len(data.payload)
        sent = self.sendto(data, server_address)
        print('ack', data.ack)  

    def sendto(self, data, address):
        return self.sock.sendto(pickle.dumps(data), address)

    def recvfrom(self):
        data, server = self.sock.recvfrom(4096)
        return pickle.loads(data), server

    def close(self):
        self.sock.close()