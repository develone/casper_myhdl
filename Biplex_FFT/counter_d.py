from myhdl import *
def ClkDriver(clk):
        halfPeriod = delay(10)
        @always(halfPeriod)
        def driveClk():
                clk.next = not clk
        return driveClk

def counter_d(count_out, clk, ena, rst, updown = 1, step = 1, MIN_COUNT = 0, MAX_COUNT = 65536 ):
    
    
    #limit = Signal(intbv()[(MAX_COUNT):MIN_COUNT])
    limit = int()
    
    if updown == 1:
        limit = MAX_COUNT
    else:
        limit = MIN_COUNT
        
    direction = Signal(bool())
    #updown_1 = updown_d(limit, direction, updown, MIN_COUNT, MAX_COUNT)
    cnt = Signal(intbv(0)[16:])
    
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
        count_out = cnt   
    return counter_logic
def convert():
        MAX_COUNT = 65536
        MIN_COUNT = 0
        count_out = Signal(intbv()[16:]) 
        cnt = Signal(intbv(0)[16:])
        updown = Signal(bool())
        ena = Signal(bool())
        rst = Signal(bool())
        clk = Signal(bool())
        step = Signal(intbv()[9:0])
        toVerilog(counter_d, count_out, clk, ena, rst, MAX_COUNT, updown, step, MIN_COUNT)

def test_bench():
        clk = Signal(0)
        ena = 1
        rst = 1
        updown = 1
        cnt  = 0
        count_out = 0
        step = 1
        counter_inst = counter_d(count_out, clk, ena, rst, MAX_COUNT = 65536, updown = 1, step = 1, MIN_COUNT = 0 )
        clkdriver_inst = ClkDriver(clk)
        #tb = traceSignals(test_bench)
        sim = Simulation(clkdriver_inst, counter_inst)
        sim.run(50)
convert()
test_bench()

