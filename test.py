from imp import reload
from CPUexecution import SymbolicExecutionEngine

sym = SymbolicExecutionEngine(0x804845A, 0x0804A17C, 0x8048000, "disass/TestDisassembler/test64", 64)
sym.run()
                                            
m = sym.get_reg_equation_simplified('edi')

print(str(m))
