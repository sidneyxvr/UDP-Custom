import socket, pickle
import sys
import time
from udp_custom import udp_custom
from timeout import timeout

class socket_custom:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__address = ('', 0)
        self.__init = 0
        self.__current_time = 0
        self.__timeout = timeout()
        self.__lastByteRead = 0

    def sendto(self, data, address):
        return self.sock.sendto(pickle.dumps(data), address)

    def recvfrom(self):
        data, server = self.sock.recvfrom(4096)
        return pickle.loads(data), server
        
    def bind(self, server_address):
        self.sock.bind(server_address)

    def close(self):
        self.sock.close()

    def confirm_ack(self, data, server_address):
        data.ack = data.seq + 1000#len(data.payload)
        sent = self.sendto(data, server_address)
        print('ack', data.ack)  
    
    def send_packet(self, data, address): #add file to constructor 
        self.__timeout.setSampleRtt(time.time() - self.__current_time)           
        self.__current_time = time.time()
        if data.ack - self.__init >= 20000: #file_size = 20000
            data.fin = 1
            sent = self.sendto(data, address)
            self.__timeout = timeout()
            return False
        data.seq = data.ack + 1
        self.__lastByteRead = data.seq 
        #fill payload
        sent = self.sendto(data, address)
        return True

    def confirm_connetion(self, data, address):
        self.__address = address
        data.ack = data.seq + 1
        self.__init = data.seq
        sent = self.sendto(data, address)

    def check_timeout(self):
        while 1:
            if(self.__timeout.timeout - self.__current_time <= 0):
                udp_ = udp_custom()
                udp_.seq = self.__lastByteRead
                #fill payload
                self.send_packet(udp_, self.__address)
            
