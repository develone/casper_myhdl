# Need to verify each design is correct, it is easiest
# to verify each of the converted files (Verilog).  By
# verifying the final result, the design, functionality,
# methodology, etc are all verified.
#
# Using Python testbenches because Python is a very flexible
# easy language (author knows well).  No need for complicated
# compile (builds) etc.

from __future__ import division
from __future__ import print_function

import os
import argparse
from argparse import Namespace
import math

from myhdl import *

def _prep_cosim(args, **sigs):
    """ prepare the cosimulation environment
    """
    # compile the verilog files with the verilog simulator
    files = ['./counter_d.v',
             './tb_counter_d.v']

    print("compiling ...")
    cmd = "iverilog -o test_counter_d %s " % (" ".join(files))

    print("  *%s" %  (cmd))
    os.system(cmd)

    # get the handle to the
    print("cosimulation setup ...")
    cmd = "vvp -m ./myhdl.vpi test_counter_d"
    return Cosimulation(cmd, **sigs)


def test_counter_d(args):
    """
    """
    DATA_WIDTH = 32768
    MAX_COUNT = Signal(fixbv(1230, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5))
    MIN_COUNT = Signal(fixbv(10, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5)) 
    cnt = Signal(fixbv(8, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5)) 
    updown = ResetSignal(0, active=0, async=True) 
    ena = ResetSignal(0, active=0, async=True) 
    rst = ResetSignal(0, active=0, async=True) 
    clk = Signal(bool(0))
    step = Signal(intbv(1)[9:])
    
    tbdut = _prep_cosim(args, cnt=cnt, clk=clk, ena=ena, rst=rst, updown=updown, step=step, MIN_COUNT=MIN_COUNT, MAX_COUNT=MAX_COUNT)
                         

    @always(delay(3))
    def tbclk():
        clk.next = not clk
    
    @instance
    def tbstim():
        yield delay(33)
        yield delay(33)
#updown lo ena lo rst lo
        cnt.next = cnt
        updown.next = ena.active
        ena.next = ena.active
        rst.next = rst.active
        yield clk.negedge

        for ii in range(5):
            print("%8d: cnt = %4x updown = %2d step = %2d ena = %2d rst = %2d MIN_COUNT = %4x MAX_COUNT = %4x" % \
                  (now(), cnt,updown,step,ena,rst,MIN_COUNT,MAX_COUNT))
            yield clk.posedge
#updown hi ena hi rst hi
        updown.next = updown.async
        ena.next = ena.async
        rst.next = rst.async
        for ii in range(2):
            print("%8d: cnt = %4x updown = %2d step = %2d ena = %2d rst = %2d MIN_COUNT = %4x MAX_COUNT = %4x" % \
                  (now(), cnt,updown,step,ena,rst,MIN_COUNT,MAX_COUNT))
            yield clk.posedge
#updown hi ena hi rst lo
        rst.next = rst.active
        for ii in range(5):
            print("%8d: cnt = %4x updown = %2d step = %2d ena = %2d rst = %2d MIN_COUNT = %4x MAX_COUNT = %4x" % \
                  (now(), cnt,updown,step,ena,rst,MIN_COUNT,MAX_COUNT))
            yield clk.posedge
#updown lo ena hi rst lo
        #cnt.next = MIN_COUNT
        updown.next = updown.active
        rst.next = rst.active
        for ii in range(10):
            print("%8d: cnt = %4x updown = %2d step = %2d ena = %2d rst = %2d MIN_COUNT = %4x MAX_COUNT = %4x" % \
                  (now(), cnt,updown,step,ena,rst,MIN_COUNT,MAX_COUNT))
            yield clk.posedge
#updown hi ena hi rst lo
        updown.next = updown.async
        rst.next = rst.active
        for ii in range(10):
            print("%8d: cnt = %4x updown = %2d step = %2d ena = %2d rst = %2d MIN_COUNT = %4x MAX_COUNT = %4x" % \
                  (now(), cnt,updown,step,ena,rst,MIN_COUNT,MAX_COUNT))
            yield clk.posedge
#updown hi ena hi rst hi
        updown.next = updown.async
        rst.next = rst.async
        for ii in range(2):
            print("%8d: cnt = %4x updown = %2d step = %2d ena = %2d rst = %2d MIN_COUNT = %4x MAX_COUNT = %4x" % \
                  (now(), cnt,updown,step,ena,rst,MIN_COUNT,MAX_COUNT))
            yield clk.posedge
#updown hi ena hi rst lo
        updown.next = updown.async
        rst.next = rst.active
        for ii in range(10):
            print("%8d: cnt = %4x updown = %2d step = %2d ena = %2d rst = %2d MIN_COUNT = %4x MAX_COUNT = %4x" % \
                  (now(), cnt,updown,step,ena,rst,MIN_COUNT,MAX_COUNT))
            yield clk.posedge

        raise StopSimulation

    print("start (co)simulation ...")
    Simulation((tbdut, tbstim, tbclk,)).run()


if __name__ == '__main__':
    test_counter_d(Namespace())
