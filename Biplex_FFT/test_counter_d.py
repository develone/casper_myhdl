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
    MAX_COUNT = Signal(fixbv(0, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5))
    MIN_COUNT = Signal(fixbv(0, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5)) 
    cnt = Signal(fixbv(0, min = -DATA_WIDTH, max = DATA_WIDTH, res= 1e-5))
    updown = Signal(bool())
    ena = Signal(bool())
    rst = Signal(bool())
    clk = Signal(bool())
    step = Signal(intbv(1)[9:])
    
    tbdut = _prep_cosim(args, cnt=cnt, clk=clk, ena=ena, rst=rst, updown=updown, step=step, MAX_COUNT=MAX_COUNT, MIN_COUNT=MIN_COUNT)
                         

    @always(delay(3))
    def tbclk():
        clk.next = not clk
    
    @instance
    def tbstim():
        rst = False
        yield delay(33)
        yield clk.negedge
        rst = not rst
        yield clk.posedge

        for ii in range(1280):
            print("%8d: mb %2d " % \
                  (now(), cnt,))
            yield clk.posedge

        raise StopSimulation

    print("start (co)simulation ...")
    Simulation((tbdut, tbstim, tbclk,)).run()


if __name__ == '__main__':
    test_counter_d(Namespace())
