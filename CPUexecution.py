from z3 import *
import re

register64 = {
    'rax' : None,
    'rbx' : None,
    'rcx' : None,
    'rdx' : None,
    'rsi' : None,
    'rdi' : None,
    'rbp' : None,
    'rsp' : None,
    'rip' : None,
    'r8'  : None,
    'r9'  : None,
    'r10' : None,
    'r11' : None,
    'r12' : None,
    'r13' : None,
    'r14' : None,
    'r15' : None
}


register32 = {
    'eax' : None,
    'ebx' : None,
    'ecx' : None,
    'edx' : None,
    'esi' : None,
    'edi' : None,
    'ebp' : None,
    'esp' : None,
    'eip' : None,
    'r8d'  : None,
    'r9d'  : None,
    'r10d' : None,
    'r11d' : None,
    'r12d' : None,
    'r13d' : None,
    'r14d' : None,
    'r15d' : None
}

register16bit = {
    'ax' : None,
    'bx' : None,
    'cx' : None,
    'dx' : None,
    'sx' : None,
    'bx' : None,
    'sx' : None,
    'ix' : None,
    'r8w'  : None,
    'r9w'  : None,
    'r10w' : None,
    'r11w' : None,
    'r12w' : None,
    'r13w' : None,
    'r14w' : None,
    'r15w' : None
}

register8bit = {
    'al' : None,
    'bl' : None,
    'cl' : None,
    'dl' : None,
    'sl' : None,
    'bl' : None,
    'sl' : None,
    'il' : None,
    'r8b'  : None,
    'r9b'  : None,
    'r10b' : None,
    'r11b' : None,
    'r12b' : None,
    'r13b' : None,
    'r14b' : None,
    'r15b' : None
}

class SymbolicExecutionEngine(object):
    def __init__(self, start, end, vbase, executable, arch):
        self.ctx = register32
        self.start = start
        self.end = end
        self.disass = open("ctf.txt")
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
        if self._check_if_reg32(r) == False:
            return
        return self.equations[self.ctx[r]]

    def memoryInstruction(self, address, mnemonic, dst, src):
        return (src in self.ctx and (dst in self.ctx and self.ctx[src])) or \
            (dst in self.ctx and (src[:1].isdigit() and int(src, 16))) or \
            (dst.find('arg_') != -1 and ((src in self.ctx and ((dst not in self.mem and None) or self.ctx[src])) or (src[:1].isdigit() and int(src,16))))
        
        if (src.find('var_') != -1 or src.find('arg')!= -1) and dst in self.ctx:
            if src not in self.mem:
                sym = BitVec('arg%d' % len(self.sym_variables), 32)
                self.sym_variables.append(sym)
                print "{0:*>20}\t{1} {2} {3}".format(address ,mnemonic, dst, src)
                self.mem[src] = self._push_equation(sym)
            return self.mem[src]
        else:
            raise Exception('{0:*>20} {1} {2} {3:*<20} is not handled.'.format(address ,mnemonic, dst, src))

    def _shr(self, dst, src):
        self.set_reg_with_equation(dst, LShR(self.get_reg_equation(dst), int(src,16)))
        
    def _shl(self, dst, src):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) << int(src, 16))

    def _and(self, dst, src):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) & ((src in self.ctx and self.get_reg_equation(src)) or int(src,16)))

    def _or(self, dst, src):
         self.set_reg_with_equation(dst, self.get_reg_equation(dst) | self.get_reg_equation(src))
           
    def _xor(self, dst, src):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) ^ self.get_reg_equation(dst))

    def _imul(self, dst, src):
            self.set_reg_with_equation(dst, self.get_reg_equation(dst) * ((src in self.ctx and self.get_reg_equation(src)) or  self.mem[src]))
            
    def _neg(self, dst):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) * -1)
                    
    def _not(self, dst, src):
        self.set_reg_with_equation(dst, ~self.get_reg_equation(dst) & 0xFFFFFFFF)

    def _sub(self, dst, src):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) - self.get_reg_equation(src))
        
    def _cdqe(self, dst, src):
        pass
    
    def _nop(self, dst, src):
        print("I'm in")
    
    def _add(self, dst, src):
            self.set_reg_with_equation(dst, self.get_reg_equation(dst) + ((src in self.ctx and self.get_reg_equation(src)) or int(src, 16))) 
    
    def run(self):
        '''Run from start address to end address the engine'''
        for line in self.disass:
            address, mnemonic, dst, src = line.split(" ")
            src = src[:-1]
            print(mnemonic, dst, src)
            if re.search("(mov)|(lea)", mnemonic):
                self.ctx[dst] = self.memoryInstruction(address, mnemonic, dst, src)
            else:
                eval("_{0}({1}, {2})".format(mnemonic, dst, src))
            
    def _simplify_additions(self, eq):
        print 
        if prove(Sum(self.sym_variables) == eq):
            return Sum(self.sym_variables)
        return eq
                        
    def get_reg_equation_simplified(self, reg):
        s = Solver()
        eq = self.get_reg_equation(reg)
        s.add(eq == 0)
        s.check()
        return s.model()

    def get_equation(self, reg):
        s = Solver()
        return self.get_reg_equation(reg)
