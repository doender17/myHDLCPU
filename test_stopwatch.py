from random import randrange

from myhdl import *

LOW, HIGH = bool(0), bool(1)
MAX_COUNT = 6 * 10 * 10
PERIOD = 10
expectations = []

@block
def TimeCount(tens, ones, tenths, startstop, reset, clock):

    @instance
    def logic():
        seen = False
        counting = False

        while True:
            yield clock.posedge, reset.posedge

            if reset:
                tens.next = 0
                ones.next = 0
                tenths.next = 0
                seen = False
                counting = False
            else:
                if startstop and not seen:
                    seen = True
                    counting = not counting
                elif not startstop:
                    seen = False

                if counting:
                    if tenths == 9:
                        tenths.next = 0
                        if ones == 9:
                            ones.next = 0
                            if tens == 5:
                                tens.next = 0
                            else:
                                tens.next = tens + 1
                        else:
                            ones.next = ones + 1
                    else:
                        tenths.next = tenths + 1

    return logic


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
        startstop.next = HIGH
        yield clock.posedge
        expectations.append((LOW, 0, 1, 0))
        yield clock.negedge
        yield clock.posedge
        raise StopSimulation

    return dut, clk, monitor, stimulus


def test_bench():
    sim = Simulation(bench())
    sim.run()
