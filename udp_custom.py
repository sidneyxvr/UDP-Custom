class udp_custom:
    def __init__(self, ack=0, syn=0, fin=0, seq=0, window_size=10, payload=""):
        self.ack = ack
        self.syn = syn
        self.fin = fin
        self.seq = seq
        self.window_size = window_size
        self.payload = payload
