from myhdl import *

@block
def alu(op, opA, opB, result, zero):

    @always_comb
    def action():
        if op == 0x0: # AND
            result.next = opA & opB
        if op == 0x1: # OR
            result.next = opA | opB
        if op == 0x2: # ADD
            result.next = opA + opB
        if op == 0x6: # SUB
            result.next = opA - opB

    @always_comb
    def zeroAction():
        if result.val == 0x0:
            zero.next = 1
        else:
            zero.next = 0

    return action, zeroAction