from myhdl import *
#BASED on a DATA_WIDTH of 18
#2**18 equals 262144
#using a res of 1e-5
#requires 35 bits
DATA_WIDTH = 262144
def ClkDriver(clk):
        halfPeriod = delay(10)
        @always(halfPeriod)
        def driveClk():
                clk.next = not clk
        return driveClk

def counter_d(cnt, clk, ena, rst, updown = 1, step = 1, MIN_COUNT = 0, MAX_COUNT = 65536 ):
    
    
    limit = int()
    
    if updown == 1:
        limit = MAX_COUNT
    else:
        limit = MIN_COUNT
        
    
    @always(clk.posedge)
    def counter_logic():
        
        if rst == 1:
            cnt.next = 0
        elif ena == 1:
            if updown == 1:
                if cnt == limit - 1:
#                    print "resetting",cnt,limit
                    cnt.next = 0
                else:
#                    print "going to add",cnt,step,limit
                    cnt.next = cnt + step
            else:
                if cnt == limit + 1:
                    cnt.next = MAX_COUNT
                else:
                    cnt.next = cnt - step
        cnt.next = cnt   
    return counter_logic
MAX_COUNT = Signal(fixbv(0, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5))
MIN_COUNT = Signal(fixbv(0, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5)) 
cnt = Signal(fixbv(0, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5))
updown = Signal(bool())
ena = Signal(bool())
rst = Signal(bool())
clk = Signal(bool())
step = Signal(intbv(1)[9:])
toVerilog(counter_d, cnt, clk, ena, rst, updown, step, MIN_COUNT, MAX_COUNT)

def test_bench():
        clk = Signal(0)
        ena = 1
        rst = 1
        updown = 1
        cnt = Signal(fixbv(0, min = -262144, max = 262144, res= 1e-5))
        step = 1
        counter_inst = counter_d(cnt, clk, ena, rst, MAX_COUNT = 65536, updown = 1, step = 1, MIN_COUNT = 0 )
        clkdriver_inst = ClkDriver(clk)
        #tb = traceSignals(test_bench)
        sim = Simulation(clkdriver_inst, counter_inst)
        sim.run(50)
#test_bench()

