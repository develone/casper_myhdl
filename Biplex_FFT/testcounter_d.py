import os
from myhdl import Cosimulation
cmd = "/usr/local/bin/iverilog -o counter_d counter_d.v tb_counter_d.v"
print cmd
def counter_d(cnt,clk,ena,rst,updown,step,MIN_COUNT,MAX_COUNT):
	os.system(cmd)
	return Cosimulation("/usr/local/bin/vvp -m ./myhdl.vpi counter_d")
