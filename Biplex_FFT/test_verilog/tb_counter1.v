module tb_counter1;
initial
 begin
    $dumpfile("tb_counter1.vcd");
    $dumpvars(0,tb_counter1);
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
  end
 /* Make a regular pulsing clock. */
  reg clk = 0;
  always #5 clk = !clk;
wire [33:0] count_out;
reg ena;


  /* Make a ena that pulses once. */
  initial begin
     # 17 ena = 1;
  end
 /* Make a regular pulsing clock. */
  always #5 clk = !clk;

counter1 dut(
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
