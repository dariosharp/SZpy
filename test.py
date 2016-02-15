from imp import reload
from CPUexecution import SymbolicExecutionEngine

sym = SymbolicExecutionEngine("testfile.ds", 64)

sym.run()
                                            
m = sym.get_solution('edi', 0)

print(str(m))
