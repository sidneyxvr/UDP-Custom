import socket, pickle
import sys
import time
from udp_custom import udp_custom
from threading import Thread

class socket_server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__address = (0, 0)
        self.__init = 0  
        self.__stablished_connection = False
        self.__last_ack = (0, 0)
        self.__last_seq_sent = 0
        self.__window_size = 1
        self.__thread = Thread()
        self.__last_ack_received = 0
        self.__timeout = 1
        self.__file_size = 3000 #bytes
        self.__payload_size = 147
        self.__payload = 'a'*self.__file_size

    def sendto(self, data, address):
        return self.sock.sendto(pickle.dumps(data), address)

    def recvfrom(self):
        data, server = self.sock.recvfrom(4096)
        data = pickle.loads(data)
        self.__last_ack_received = data.ack
        return data, server        
        
    def bind(self, server_address):
        self.sock.bind(server_address)

    def close(self):
        self.sock.close()

    def confirm_connetion(self, data, address):
        self.__address = address
        self.__stablished_connection = True
        data.ack = data.seq
        self.__init = data.seq + 1
        self.__last_ack = (data.seq, 1)
        self.__last_seq_sent = data.seq + 1
        sent = self.sendto(data, address)
        self.sock.settimeout(1)
        data, address = self.recvfrom()
        self.__thread = Thread(target=self.sendpack)
        self.__thread.start()
           
    def resendpack(self):
        udp_ = udp_custom()
        udp_.seq = self.__last_ack_received
        self.__last_ack = (self.__last_ack[0], 0)
        udp_.payload = self.__payload[self.__last_ack_received - self.__init: (self.__last_ack_received - self.__init) + self.__payload_size]
        print('reenviado', udp_.seq)
        sent = self.sendto(udp_, self.__address)
        
        
    def recvpack(self):
        while 1:
            try:
                data, address = self.recvfrom()
                print('confirmado', data.ack)
                if data.syn == 1:
                    self.confirm_connetion(data, address)
                else:
                    if self.__init + self.__file_size <= self.__last_ack_received:
                        while data.fin != 1:
                            data.fin = 1
                            data.payload = ''
                            self.sendto(data, address)
                            data, server = self.recvfrom()
                        return
                    if data.ack > self.__last_ack[0]:
                        self.__timeout -= self.__timeout * 0.05
                        self.sock.settimeout(min(self.__timeout, 5))
                        self.__last_ack = (data.ack, 1)
                        self.__window_size += 1
                        continue
                    elif data.ack == self.__last_ack[0]:
                        self.__last_ack = self.__last_ack[0], self.__last_ack[1] + 1
                        if self.__last_ack[1] == 3:
                            print('ack duplicado', data.ack)
                            self.resendpack()
                            self.sock.settimeout(min(self.__timeout, 5))
                            self.__window_size = (int)(self.__window_size / 2)
                            continue
            except:
                print('timeout', min(self.__timeout, 5))
                self.resendpack()
                self.__window_size = 1
                self.__timeout += self.__timeout * 0.20
                self.sock.settimeout(min(self.__timeout, 5))
                    
    def sendpack(self):
        while 1:
            if self.__stablished_connection == True:                  
                #pacotes em transito                                 #capacidade de envio em bytes
                if self.__last_seq_sent - self.__last_ack_received < self.__window_size * self.__payload_size:
                    data = udp_custom()
                    data.seq = self.__last_seq_sent
                    if self.__last_seq_sent - self.__init < self.__file_size:
                        print('enviado', data.seq)
                        data.payload = self.__payload[self.__last_seq_sent - self.__init: (self.__last_seq_sent - self.__init) + self.__payload_size]
                        self.__last_seq_sent += self.__payload_size
                        self.sendto(data, self.__address)
                    else:
                        return