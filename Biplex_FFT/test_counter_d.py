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
    DATA_WIDTH = 262144
    MAX_COUNT = Signal(fixbv(1230, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5))
    MIN_COUNT = Signal(fixbv(10, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5)) 
    cnt = Signal(fixbv(0, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5))
    updown = Signal(bool(0))
    ena = Signal(bool(1))
    rst = Signal(bool(0))
    clk = Signal(bool(0))
    step = Signal(intbv(1)[9:])
    
    tbdut = _prep_cosim(args, cnt=cnt, clk=clk, ena=ena, rst=rst, updown=updown, step=step, MAX_COUNT=MAX_COUNT, MIN_COUNT=MIN_COUNT)
                         

    @always(delay(3))
    def tbclk():
        clk.next = not clk
    
    @instance
    def tbstim():
#        ena = False
        rst = False 
        updown = False
        yield delay(33)
        rst = True 
        yield clk.negedge
        ena = True 
        yield clk.posedge
        rst = 0 

        for ii in range(12):
            ena = True
            rst = True 
            print("%8d: cnt = %2d updown = %2d step = %2d ena = %2d rst = %2d" % \
                  (now(), cnt,updown,step,ena,rst))
            yield clk.posedge
        for ii in range(12):
            ena = True
            rst = True
            updown = True
            print("%8d: cnt = %2d updown = %2d step = %2d ena = %2d rst = %2d" % \
                  (now(), cnt,updown,step,ena,rst))
            yield clk.posedge
        for ii in range(12):
            ena = True
            rst = False
            print("%8d: cnt = %2d updown = %2d step = %2d ena = %2d rst = %2d" % \
                  (now(), cnt,updown,step,ena,rst))
            yield clk.posedge

        raise StopSimulation

    print("start (co)simulation ...")
    Simulation((tbdut, tbstim, tbclk,)).run()


if __name__ == '__main__':
    test_counter_d(Namespace())
