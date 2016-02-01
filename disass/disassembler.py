#!/usr/bin/python2.7 disassembler.py

from capstone import *
from capstone.x86 import *


operX86 = (
    (X86_OP_REG, (lambda insn, i : insn.reg_name(i.reg))),
    (X86_OP_IMM, (lambda insn, i:  "%s" % (hex((i.imm))))),
    (X86_OP_FP, (lambda insn, i : "%f" % (i.fp))),
    (X86_OP_MEM, (lambda insn, i: "".join([func(insn, i) for (search, func) in operX86inMem if search(i) == True]) + "]"))
)

operX86inMem = (
    ((lambda i : True if i.mem.segment != 0 else False), (lambda insn, i: "%s:[" % (insn.reg_name(i.mem.segment)))),
    ((lambda i : True if i.mem.segment == 0 else False), (lambda insn, i: "[")),
    ((lambda i : True if i.mem.base != 0 else False), (lambda insn, i: "%s" % (insn.reg_name(i.mem.base)))),
    ((lambda i : True if i.mem.index != 0 else False), (lambda insn, i: "%s" % (insn.reg_name(i.mem.index)))),
    ((lambda i : True if i.mem.scale != 1 else False), (lambda insn, i: "*%u" % (i.mem.scale))),
    ((lambda i : True if i.mem.disp != 0 else False), (lambda insn, i: "+arg_%s" % str(hex((i.mem.disp)))[2:])),
    ((lambda i : True if i.mem.disp == 0 else False), (lambda insn, i: "+arg_0"))
     
    )

arch = {
    32: (operX86, X86_AVX_BCAST_INVALID, X86_INS_RET, CS_MODE_32),
    64: (operX86, X86_AVX_BCAST_INVALID, X86_INS_RET, CS_MODE_64)
}


class Disassembler(object):
    ''' Class to disassemble function, value needed are: 
    -> address of start disasseble
    -> address of end Disassemble
    -> address of VirtAddr start
    -> file to disassemble
    -> architecture type (32 or 64 bit)
    
    ----------------------------------
    -> store_istruction() to save disassembled into file
    -> __str__ to ptint disassembled
    -> decode() to iterate
    '''

    def __init__(self, vstart, vend, vbase, executable, architecture) :
        self.executable = open(executable, 'rb').read()
        self.start = vbase
        self.end = vend
        self.rip = vstart - vbase
        self.arch = architecture
        self.md = Cs(CS_ARCH_X86, arch[self.arch][3])
        self.md.detail = True

    def _decode_operandos(self):
        ''' Decode and split operandos '''
        insn = self.md.disasm(self.executable[self.rip:self.rip+16],
                      self.rip + self.start)
        insn = next(insn)
        self.rip += insn.size
        op = ["", ""]
        c = -1
        for i in insn.operands:
            c += 1
            for (search, func) in arch[self.arch][0]:
                if i.type == search:
                    op[c] += func(insn, i)
            if i.avx_bcast != arch[self.arch][1]:
                op[c]="%u" % (i.avx_bcast)
        if insn.id == arch[self.arch][2]:
            self.end = self.rip + self.start
        return(insn.address, insn.mnemonic, op[0], op[1])
        
    def decode(self):
        while self.rip != (self.end - self.start):
            yield self._decode_operandos()
            
    def store_istruction(self, store_file):
        ''' Save all istruction as string'''
        string_istruction = ''
        for add, mn, op0, op1 in self.decode():
            string_istruction += "0x{0:x} {1} {2} {3}\n".format(add, mn, op0, op1)
            open(store_file, 'wb').write(string_istruction)

    def __str__(self):
        string_istruction = ''
        for add, mn, op0, op1 in self.decode():
            string_istruction += "0x{0:x}\t{1}\t{2} {3}\n".format(add, mn, op0, op1)
        return string_istruction
