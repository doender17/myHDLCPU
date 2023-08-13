from myhdl import *
from examples.TimeCount import TimeCount

LOW, HIGH = bool(0), bool(1)
MAX_COUNT = 6 * 10 * 10
PERIOD = 10
expectations = []

@block
def bench():
    tens, ones, tenths = [Signal(intbv(0)[4:]) for s in range(3)]
    startstop, reset, clock = [Signal(LOW) for s in range(3)]

    dut = TimeCount(tens, ones, tenths, startstop, reset, clock)

    count = Signal(0)
    counting = Signal(False)

    @always(delay(PERIOD // 2))
    def clk():
        clock.next = not clock
        return clock

    @always(clock.negedge)
    def monitor():
        global expectations
        while True:
            try:
                e = expectations.pop()
            except IndexError:
                break
            print("Expectation : %s" % str(e))
            assert e[0] == reset.val
            assert e[1] == tens
            assert e[2] == ones
            assert e[3] == tenths

    @instance
    def stimulus():
        reset.next = HIGH
        global expectations
        expectations.append((HIGH, 0, 0, 0))
        yield clock.negedge
        reset.next = LOW
        startstop.next = HIGH
        yield clock.posedge
        expectations.append((LOW, 0, 0, 1))
        yield clock.negedge
        startstop.next = LOW
        for i in range(8):
            yield clock.posedge
            expectations.append((LOW, 0, 0, i+2 ))
            yield clock.negedge
        yield clock.posedge
        expectations.append((LOW, 0, 1, 0))
        yield clock.negedge
        for i in range(89):
            yield clock.posedge
            yield clock.negedge
        yield clock.posedge
        expectations.append((LOW, 1, 0, 0))
        yield clock.negedge

        for i in range(499):
            yield clock.posedge
            yield clock.negedge

        yield clock.posedge
        expectations.append((LOW, 0, 0, 0))
        yield clock.negedge

        raise StopSimulation

    return dut, clk, monitor, stimulus


def test_bench():
    b = bench()
    sim = Simulation(b)
    traceSignals.tracebackup = False
    traceSignals.directory = "../traces"
    traceSignals.filename = "TimeCount"
    traceSignals(b)
    sim.run()
