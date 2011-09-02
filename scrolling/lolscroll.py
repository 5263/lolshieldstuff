#!/usr/bin/env python
import serial,time

def group(string, n):
    """Splits a string into smaller substrings of character length n
    From: http://snippets.dzone.com/posts/show/5641 """
    return [string[i:i+n] for i in xrange(0, len(string), n)]

class Lolscroll:
    def __init__(self,portname='/dev/ttyUSB0'):
        self.port=serial.Serial(portname,9600,timeout=10000)
    def getbufferstatus(self):
        if self.port.inWaiting():
            statusbyte=self.port.read(self.port.inWaiting())[-1]
            if statusbyte.isdigit():
                return int(statusbyte)
            elif statusbyte.isalpha():
                return (ord(statusbyte)-61)<<4

    def write(self,str1):
        for part in group(str1,16):
            time.sleep(0.05)
            while self.getbufferstatus() < 128:
                time.sleep(0.1)
            #print part
            self.port.write(part.encode('latin1','replace'))

if __name__ == '__main__':
    lolscroll=Lolscroll()
    while True:
        lolscroll.write('%s\x17 '%raw_input().decode('utf8'))


