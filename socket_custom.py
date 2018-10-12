import socket, pickle
import sys
import time
from udp_custom import udp_custom
from timeout import timeout
from threading import Semaphore, Thread, Event, Condition

class socket_custom:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__address = (0, 0)
        self.__init = 0  
        self.__stablished_connection = False
        self.__lastAck = (0, 0)
        self.__lastSeqSend = 0
        self.__window_size = 10
        self.__thread = Thread()
        self.__ultima_ack_recebido = 0
        

    def sendto(self, data, address):
        return self.sock.sendto(pickle.dumps(data), address)

    def recvfrom(self):
        data, server = self.sock.recvfrom(4096)
        data = pickle.loads(data)
        self.__ultima_ack_recebido = data.ack
        return data, server        
        
    def bind(self, server_address):
        self.sock.bind(server_address)

    def close(self):
        self.sock.close()

    def check_ack(self, ack):
        if ack > self.__lastAck[0]:
            self.__lastAck = (ack, 0)
            return False
        elif ack == self.__lastAck[0]:
            self.__lastAck[1] += 1
            return True
        else:
            return True

    def confirm_connetion(self, data, address):
        self.__address = address
        self.__stablished_connection = True
        data.ack = data.seq + 1
        self.__init = data.seq
        self.__lastAck = (data.seq, 0)
        self.__lastSeqSend = data.seq
        sent = self.sendto(data, address)
        self.sock.settimeout(1)
        self.__thread = Thread(target=self.sendpack)
        self.__thread.start()
           
    def resendpack(self):
        udp_ = udp_custom()
        udp_.seq = self.__ultima_ack_recebido
        self.__lastAck = (self.__lastAck[0], 0)
        sent = self.sendto(udp_, self.__address)
        print('resent', udp_.seq)

    def recvpack(self):
        while 1:
            try:
                data, address = self.recvfrom()
                if self.__lastAck == data.ack:
                    return  
                print('pack',data.ack)
                if self.__init + 20000 < self.__ultima_ack_recebido + 50:
                    data.fin = 1
                    self.sendto(data, address)
                    return
                if data.syn == 1:
                    self.confirm_connetion(data, address)
                else:
                    if data.ack > self.__lastAck[0]:
                        self.__lastAck = (data.ack, 1)
                        continue
                    elif data.ack == self.__lastAck[0]:
                        self.__lastAck = self.__lastAck[0], self.__lastAck[1] + 1
                        if self.__lastAck[1] == 3:
                            self.resendpack()
                            continue
            except:
                self.resendpack()
                print('timeout ^')
                self.sock.settimeout(0.8)
                    
    def sendpack(self):
        while 1:
            if self.__stablished_connection == True:
                data = udp_custom()
                data.seq = self.__lastSeqSend #=============
                print('sendpack',data.seq)
                if self.__lastSeqSend - self.__init < 20000:
                    sent = self.sendto(data, self.__address)
                    self.__lastSeqSend += 1000
                else:
                    return