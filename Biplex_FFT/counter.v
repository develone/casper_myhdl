// File: counter.v
// Generated by MyHDL 0.9dev
// Date: Thu Jun  5 13:01:13 2014


`timescale 1ns/10ps

module counter (
    count_out,
    clk,
    ena,
    rst,
    updown
);


output signed [16:0] count_out;
reg signed [16:0] count_out;
input clk;
input ena;
input rst;
input updown;

reg [16:0] cnt;





always @(posedge clk) begin: COUNTER_COUNTER_LOGIC
    if ((rst == 1)) begin
        cnt <= 0;
    end
    else if ((ena == 1)) begin
        if ((updown == 1)) begin
            if (($signed({1'b0, cnt}) == (20 - 1))) begin
                cnt <= 0;
            end
            else begin
                cnt <= (cnt + 1);
            end
        end
        else begin
            if ((cnt == (20 + 1))) begin
                cnt <= 200;
            end
            else begin
                cnt <= (cnt - 1);
            end
        end
    end
    count_out <= cnt;
end

endmodule
