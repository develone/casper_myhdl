module tb_counter;

wire [16:0] count_out;
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

counter dut(
    count_out,
    clk,
    ena,
    rst,
    updown
);

endmodule
