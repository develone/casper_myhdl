module tb_counter;

initial
 begin
    $dumpfile("tb_counter.vcd");
    $dumpvars(0,tb_counter);
 end

  /* Make a updown that pulses once. */
  reg updown = 0;
  initial begin
     # 27 updown = 1;
     # 11 updown = 0;
     # 29 updown = 1;
     # 100 $stop;
  end
  /* Make a rst that pulses once. */
  reg rst = 0;
  initial begin
     # 17 rst = 1;
     # 11 rst = 0;
     # 29 rst = 1;
     # 11 rst = 0;
     # 100 $stop;
  end

  /* Make a ena that pulses once. */
  reg ena = 0;
  initial begin
     # 17 ena = 1;
  end
 /* Make a regular pulsing clock. */
  reg clk = 0;
  always #5 clk = !clk;

wire [16:0] count_out;


counter dut(
    count_out,
    clk,
    ena,
    rst,
    updown
);
 initial
     $monitor("At time %t, count_out  = %h (%0d)",
              $time, count_out, count_out);

endmodule
