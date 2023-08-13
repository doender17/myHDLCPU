from myhdl import *
from riscv import registerbank

LOW, HIGH = bool(0), bool(1)
REGADDRBITS = 5
CPUBITS = 32
PERIOD = 10

@block
def bench():
    readRegA, readRegB, writeReg = [Signal(intbv(0)[REGADDRBITS:]) for i in range(3)]
    dataA, dataB, dataW = [Signal(intbv(0)[CPUBITS:]) for i in range(3)]
    clock = Signal(LOW)
    writeEnable = Signal(LOW)
    dut = registerbank.registerbank(clock, writeEnable, readRegA, readRegB, writeReg, dataA, dataB, dataW)

    @always(delay(PERIOD // 2))
    def clk():
        clock.next = not clock
        return clock

    @instance
    def stimulus():
        # Read initial values
        for i in range(32):
            readRegA.next = i
            readRegB.next = 31 - i
            yield clock.negedge
            assert 10 + i, dataA.val
            assert 31 + 10 -1, dataB.val

        # Write a value
        writeEnable.next = HIGH
        writeReg.next = 0xA
        dataW.next = 100
        readRegA.next = 0xA
        yield clock.negedge
        assert 100, dataA.val

        raise StopSimulation

    return dut, clk, stimulus
def test_bench():
    b = bench()
    sim = Simulation(b)
    traceSignals.tracebackup = False
    traceSignals.directory = "../traces"
    traceSignals.filename = "registerbank"
    traceSignals(b)
    sim.run()
