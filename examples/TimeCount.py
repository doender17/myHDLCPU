from myhdl import *
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
