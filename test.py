from imp import reload
from CPUexecution import SymbolicExecutionEngine

sym = SymbolicExecutionEngine("name_file.ds", 64)

sym.run()
                                            
m = sym.get_solution('edi', 34)

print(str(m))
