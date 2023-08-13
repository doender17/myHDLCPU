from myhdl import *
LOW, HIGH = bool(0), bool(1)

@block
def registerbank(clk, writeEnable, readRegA, readRegB, writeReg, readDataA, readDataB, writeData):

    registers = [Signal(intbv(10 + i)[32:]) for i in range(32)]

    @always_comb
    def action():
        readDataA.next = registers[readRegA]
        readDataB.next = registers[readRegB]

    @always(clk.posedge)
    def actionWrite():
        if (writeEnable.val == HIGH):
            registers[writeReg].next = writeData

    return action, actionWrite