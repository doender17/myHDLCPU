from examples.blinky import blinky
from myhdl import *

def test_convert():
    clk = Signal(bool(0))
    led = Signal(intbv(0)[4:])

    conv_inst = blinky(clk, led)
    conv_inst.convert(hdl='Verilog', testbench=None)