module tb_counter_d;

wire [35:0] cnt;
reg clk;
reg ena;
reg rst;
reg updown;
reg [8:0] step;
reg [35:0] MIN_COUNT;
reg [35:0] MAX_COUNT;

initial begin
    $dumpfile("vcd/counter_d.vcd");
    $dumpvars(0, tb_counter_d);
end
initial begin
    $from_myhdl(
        clk,
        ena,
        rst,
        updown,
        step,
        MIN_COUNT,
        MAX_COUNT
    );
    $to_myhdl(
        cnt
    );
end

counter_d dut(
    cnt,
    clk,
    ena,
    rst,
    updown,
    step,
    MIN_COUNT,
    MAX_COUNT
);

endmodule
