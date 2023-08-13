from myhdl import *
from random import randrange

tmp = intbv(0)
print(len(tmp))
print(len(tmp[4:]))
@block
def dff(q, d, clk):

    @always(clk.posedge)
    def logic():
        q.next = d

    return logic

@block
def test_dff():

    q, d, clk = [Signal(bool(0)) for i in range(3)]

    dff_inst = dff(q, d, clk)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @always(clk.negedge)
    def stimulus():
        d.next = randrange(2)

    return dff_inst, clkgen, stimulus


def simulate(timesteps):
    simInst = test_dff()
    simInst.config_sim(trace=True, tracebackup=False)
    simInst.run_sim(timesteps, quiet=0)

simulate(2000)