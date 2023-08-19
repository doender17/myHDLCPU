from myhdl import *
@block
def blinky(CLK12MHZ, led):

    counter = Signal(intbv(0)[25:])

    @always(CLK12MHZ.posedge)
    def process():
        led.next[0] = counter[24]
        led.next[1] = counter[23]
        led.next[2] = counter[22]
        led.next[3] = counter[21]
        counter.next = counter + 1

    return process