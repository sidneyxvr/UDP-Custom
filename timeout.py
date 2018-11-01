import time

class Timeout:
    def __init__(self, timeout = 0.0, devRtt = 0.0, estimatedRtt = 0.0, sampleRtt = 0.0):
        self.timeout = 1
        self.devRtt = devRtt
        self.estimatedRtt = estimatedRtt
        self.sampleRtt = sampleRtt
        self.hole = False
        self.__lastTime = 0.0
        self.__current_time = 0

    def setSampleRtt(self, current_time):
        if self.hole == True:
            self.sampleRtt = current_time
        self.refresh()
        self.__lastTime = time.time()

    def refresh(self):
        if self.hole == True:
            self.estimatedRtt = 0.875 * self.estimatedRtt + 0.125 * self.sampleRtt
            self.devRtt = 0.75 * self.devRtt + abs(self.sampleRtt - self.estimatedRtt)
            self.timeout = self.estimatedRtt + 4 * self.devRtt
        self.hole = True

    def check(self):
        if(self.timeout - (time.time() - self.__lastTime) <= 0.0):
            return True
        return False

    def double_timeout(self):
        print('antes',self.timeout)
        self.timeout *= 2.0
        print('depois',self.timeout)
        