module tb_counter1;

wire [33:0] count_out;
reg clk;
reg ena;
reg rst;
reg updown;

initial begin
    $from_myhdl(
        clk,
        ena,
        rst,
        updown
    );
    $to_myhdl(
        count_out
    );
end

counter1 dut(
    count_out,
    clk,
    ena,
    rst,
    updown
);

endmodule
