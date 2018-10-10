import socket, pickle
import sys
import time
from udp_custom import udp_custom
from timeout import timeout
from threading import Semaphore, Thread

class socket_custom:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__address = ('', 0)
        self.__init = 0
        self.__current_time = 0
        self.__timeout = timeout()
        self.__lastByteRead = 0
        self.__stablished_connection = False
        self.__lastAck = (0, 0)
        self.__mtx = Semaphore()
        self.__thread = Thread(target=self.check_timeout)
        self.__thread.start()

    def sendto(self, data, address):
        return self.sock.sendto(pickle.dumps(data), address)

    def recvfrom(self):
        data, server = self.sock.recvfrom(4096)
        return pickle.loads(data), server
        
    def bind(self, server_address):
        self.sock.bind(server_address)

    def close(self):
        self.sock.close()
    
    def send_packet(self, data, address): #add file to constructor 
        self.__timeout.setSampleRtt(time.time() - self.__current_time)           
        self.__current_time = time.time()
        self.__stablished_connection = True
        if data.ack > self.__lastAck[0]:
            self.__lastAck = (data.ack, 0)
        elif data.ack == self.__lastAck[0]:
            self.__lastAck = (data.ack, self.__lastAck + 1)
            return True
        else:
            return True
        if data.ack - self.__init >= 20000: #file_size = 20000
            data.fin = 1
            sent = self.sendto(data, address)
            self.__timeout = timeout()
            self.__mtx.acquire()
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
        while True:
            # print('merda')
            if self.__stablished_connection:
                time.sleep(0.1)
                self.__mtx.acquire()
                # print('nada')
                if(self.__timeout.check() == True):
                    self.__timeout.double_timeout()
                    udp_ = udp_custom()
                    udp_.seq = self.__lastByteRead
                    #fill payload
                    self.send_packet(udp_, self.__address)
                    self.__timeout.hole = False #func
                    print('resent', udp_.seq)
                self.__mtx.release()
            