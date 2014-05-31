from myhdl import *

def ROM(dout, addr, CONTENT):
    
    @always_comb
    def read():
        dout.next = CONTENT[int(addr)]

    return read
