from z3 import *
from register_convert import *
import re



class SymbolicExecutionEngine(object):
    def __init__(self, file_disass, arch):
        self.ctx = register(r64)
        self.disass = open(file_disass)
        self.mem = {}
        self.idx = 0
        self.sym_variables = []
        self.equations = {}

    def _push_equation(self, e):
        self.equations[self.idx] = e
        self.idx += 1
        return (self.idx - 1)

    def set_reg_with_equation(self, r, e):
        self.ctx[r] = self._push_equation(e)

    def get_reg_equation(self, r):
        return self.equations[self.ctx[r]]

    def memoryInstruction(self, mnemonic, dst, src):
        
        if (src in allreg and dst in allreg):
            self.ctx[dst] = self.ctx[src]
            return
        
        if (dst in allreg and src[:1].isdigit()):
            self.ctx[dst] = int(src, 16)
            return
        
        if (dst.find('arg_') != -1):
            if (src in allreg):
                self.mem[dst] =  self.ctx[src]
        
            if (src[:1].isdigit()):
                self.mem[dst] =  int(src,16)
            return

        if (src.find('var_') != -1 or src.find('arg')!= -1) and dst in allreg:
            if src not in self.mem:
                sym = BitVec('arg{}'.format(len(self.sym_variables)), ((dst in r64 and 64) or (dst in r32 and 32)
                                                                       or (dst in r16 and 16) or (dst in r8 and 8)))
                self.sym_variables.append(sym)
                print "*** {0} {1} {2} ***".format(mnemonic, dst, src)
                self.mem[src] = self._push_equation(sym)
            self.ctx[dst] =  self.mem[src]
            return
        
        raise Exception('{:*>20} {0} {1} {2:*<20} is not handled.'.format(mnemonic, dst, src))

    def _mov(self, dst, src):
        self.memoryInstruction("mov", dst, src)
        
    def _lea(self, dst, src):
        self.memoryInstruction("mov", dst, src)

    def _movsx(self, dst, src):
        self.memoryInstruction("mov", dst, src)
        
    def _shr(self, dst, src):
        self.set_reg_with_equation(dst, LShR(self.get_reg_equation(dst), int(src,16)))
        
    def _shl(self, dst, src):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) << int(src, 16))

    def _and(self, dst, src):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) & ((src in allreg and self.get_reg_equation(src)) or int(src,16)))

    def _or(self, dst, src):
         self.set_reg_with_equation(dst, self.get_reg_equation(dst) | self.get_reg_equation(src))
           
    def _xor(self, dst, src):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) ^  ((src[:1].isdigit() and int(src, 16)) or self.get_reg_equation(src)))

    def _imul(self, dst, src):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) * ((src in allreg and self.get_reg_equation(src)) or self.mem[src]))
            
    def _neg(self, dst=None, src=None):
        self.set_reg_with_equation(dst, self.get_reg_equation(src) * -1)
                    
    def _not(self, dst, src=None):
        self.set_reg_with_equation(dst, ~self.get_reg_equation(dst) & 0xFFFFFFFF)

    def _sub(self, dst, src):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) -  ((src[:1].isdigit() and int(src, 16)) or self.get_reg_equation(src)))
        
    def _cdqe(self, dst, src):
        pass
    
    def _nop(self, dst, src):
        pass
    
    def _add(self, dst, src):
        self.set_reg_with_equation(dst, self.get_reg_equation(dst) + ((src[:1].isdigit() and int(src, 16)) or self.get_reg_equation(src))) 
    
    def run(self):
        for line in self.disass:
            address, mnemonic, dst, src = line.split(" ")
            # print(mnemonic, dst, src)
            eval("self._{0}('{1}', '{2}')".format(mnemonic, dst, src[:-1]))
            
    def get_solution(self, reg, value):
        s = Solver()
        eq = self.get_reg_equation(reg)
        s.add(eq == value)
        s.check()
        return s.model()
