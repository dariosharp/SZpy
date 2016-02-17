from z3 import *
from register_convert import register
from instruction import instruction


class SymbolicExecutionEngine(instruction):
    def __init__(self, file_disass):
        self.ctx = register()
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
    
    def clear_dict(self, d):
        for i in range(0, len(d), 2):
            del d[i]
        return d
                    

    def get_string_solution(self, output):
        s = Solver()
        eq = self.clear_dict(self.equations)
        s.add(*[eq[x]== ord(y) for x, y in zip(eq, output)])
        s.check()
        return s.model()
