from disass.disassembler import Disassembler
from z3 import *


registerX86 = {
    'eax' : None,
    'ebx' : None,
    'ecx' : None,
    'edx' : None,
    'esi' : None,
    'edi' : None,
    'ebp' : None,
    'esp' : None,
    'eip' : None
}

register16bit = {
    'al' : None,
    'bl' : None,
    'cl' : None,
    'dl' : None,
    'sl' : None,
    'bl' : None,
    'sl' : None,
    'il' : None
}


class SymbolicExecutionEngine(object):
    def __init__(self, start, end, vbase, executable, arch):
        self.ctx = {
            'eax' : None,
            'ebx' : None,
            'ecx' : None,
            'edx' : None,
            'esi' : None,
            'edi' : None,
            'ebp' : None,
            'esp' : None,
            'eip' : None
        }

        self.start = start
        self.end = end
        self.disass = Disassembler(start, end, vbase, executable, arch)
        self.mem = {}
        self.idx = 0
        self.sym_variables = []
        self.equations = {}

    def _check_if_reg32(self, r):
        '''XXX: make a decorator?'''
        return r.lower() in self.ctx

    def _push_equation(self, e):
        self.equations[self.idx] = e
        self.idx += 1
        return (self.idx - 1)

    def set_reg_with_equation(self, r, e):
        if self._check_if_reg32(r) == False:
            return
        self.ctx[r] = self._push_equation(e)

    def get_reg_equation(self, r):
        #print self.sym_variables
        if self._check_if_reg32(r) == False:
            return
        return self.equations[self.ctx[r]]

    def run(self):
        '''Run from start address to end address the engine'''
        for address, mnemonic, dst, src in self.disass.decode():
            if dst == 'al':
                dst = 'eax'
            if dst == 'cl':
                dst = 'ecx'
            if src == 'al':
                src = 'eax'
            if src == 'cl':
                src = 'ecx'
            if mnemonic == 'mov' or mnemonic == 'movsx':
                # mov reg32, reg3
                if src in self.ctx and dst in self.ctx:
                    self.ctx[dst] = self.ctx[src]
                # mov reg32, [mem]
                elif (src.find('var_') != -1 or src.find('arg')!= -1) and dst in self.ctx:
                    if src not in self.mem:
                        #print src
                        # A non-initialized location is trying to be read, we got a symbolic variable!
                        sym = BitVec('arg%d' % len(self.sym_variables), 32)
                        self.sym_variables.append(sym)
                        print "{0}\t{1}\t{2}\t{3}".format(hex(address),mnemonic, dst, src)
                        #print 'Trying to read a non-initialized area, we got a new symbolic variable: %s' % sym
                        
                        self.mem[src] = self._push_equation(sym)
                    
                    self.ctx[dst] = self.mem[src]
                # mov [mem], reg32
                elif dst.find('arg_') != -1 and src in self.ctx:
                    if dst not in self.mem:
                        self.mem[dst] = None
                    self.mem[dst] = self.ctx[src]
                else:
                    print mnemonic, dst, src
                    raise Exception('This encoding of "mov" is not handled.')
            elif mnemonic == 'shr':
                # shr reg32, cst
                # dst, src
                if dst in self.ctx:
                    if type(src) == int:
                        self.set_reg_with_equation(dst, LShR(self.get_reg_equation(dst), src))
                    else:
                        self.set_reg_with_equation(dst, LShR(self.get_reg_equation(dst), int(src,16)))
                else:
                    raise Exception('This encoding of "shr" is not handled.')
            elif mnemonic == 'shl':
                # shl reg32, cst
                if dst in self.ctx:
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) << int(src, 16))
                else:
                    raise Exception('This encoding of "shl" is not handled.')
            elif mnemonic == 'and':
                x = None
                # and reg32, reg32
                if src in self.ctx:
                    x = self.get_reg_equation(src)
                # and reg32, cst
                else:
                    x = int(src, 16)
                self.set_reg_with_equation(dst, self.get_reg_equation(dst) & x)
            elif mnemonic == 'xor':
                # xor reg32, cst
                if dst in self.ctx:
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) ^ int(src, 16))
                else:
                    raise Exception('This encoding of "xor" is not handled.')
            elif mnemonic == 'or':
                # or reg32, reg32
                if dst in self.ctx and src in self.ctx:
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) | self.get_reg_equation(src))
                else:
                    raise Exception('This encoding of "or" is not handled.')
            elif mnemonic == 'add':
                # add reg32, reg32
                if dst in self.ctx and src in self.ctx:
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) + self.get_reg_equation(src))
                elif dst in self.ctx:
                    self.set_reg_with_equation(dst, self.get_reg_equation(dst) + int(src, 16))
                else:
                    raise Exception('This encoding of "add" is not handled.')
            else:
                print mnemonic, dst, src
                raise Exception('This instruction is not handled.')
            
    def _simplify_additions(self, eq):
        print 
        if prove(Sum(self.sym_variables) == eq):
            return Sum(self.sym_variables)
        return eq
                        
    def get_reg_equation_simplified(self, reg):
        s = Solver()
        eq = self.get_reg_equation(reg)
        s.add(eq == 5)
        s.check()
        return s.model()

    def get_equation(self, reg):
        s = Solver()
        return self.get_reg_equation(reg)
