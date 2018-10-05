import time

class timeout:
    def __init__(self, timeout = 0.0, devRtt = 0.0, estimatedRtt = 0.0, sampleRtt = 0.0):
        self.timeout = timeout
        self.devRtt = devRtt
        self.estimatedRtt = estimatedRtt
        self.sampleRtt = sampleRtt
        self.hole = False

    def setSampleRtt(self, time):
        if self.hole == True:
            self.sampleRtt = time
        self.refresh()

    def refresh(self):
        if self.hole == True:
            self.estimatedRtt = 0.875 * self.estimatedRtt + 0.125 * self.sampleRtt
            self.devRtt = 0.75 * self.devRtt + abs(self.sampleRtt - self.estimatedRtt)
            self.timeout = self.estimatedRtt + 4 * self.devRtt
        self.hole = True
        print('timeout', self.timeout)