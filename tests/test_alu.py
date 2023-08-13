from myhdl import *
from riscv import alu

LOW, HIGH = bool(0), bool(1)
CPUBITS = 32
PERIOD = 10

@block
def bench():
    opcode = Signal(intbv(0)[4:])
    opA, opB, result = [Signal(intbv(0)[CPUBITS:]) for i in range(3)]
    zero = Signal(intbv(0)[1:])
    clock = Signal(LOW)
    dut = alu.alu(opcode, opA, opB, result, zero)

    @always(delay(PERIOD // 2))
    def clk():
        clock.next = not clock
        return clock

    @instance
    def stimulus():
        yield clock.negedge
        # AND
        opcode.next =0x0
        opA.next = 0xFFFE
        opB.next = 3
        yield clock.negedge
        assert 2 == result.val
        assert 0 == zero.val
        # OR
        opcode.next =0x1
        opA.next = 0x1110
        opB.next = 3
        yield clock.negedge
        assert 0x1113 == result.val
        assert 0 == zero.val

        # Add
        opcode.next = 0x2
        opA.next = 4
        opB.next = 6
        yield clock.negedge
        assert 10 == result.val
        assert 0 == zero.val
        # Subtract
        opcode.next = 0x6
        opA.next = 10
        opB.next = 9
        yield clock.negedge
        assert 1 == result.val
        assert 0 == zero.val
        opB.next = 10
        yield clock.negedge
        assert 0 == result.val
        assert 1 == zero.val
        raise StopSimulation

    return dut, clk, stimulus
def test_bench():
    b = bench()
    sim = Simulation(b)
    traceSignals.tracebackup = False
    traceSignals.directory = "../traces"
    traceSignals.filename = "ALU"
    traceSignals(b)
    sim.run()
