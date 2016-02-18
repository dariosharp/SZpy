'''
This tool is based on z3 with Symbolic Execution. 

compile llvm: "clang -static"

For all news follow me @dariosharp
'''

#################################
#				#
#	Execution Example	#
#				#
#################################

from imp import reload
from CPUexecution import SymbolicExecutionEngine


def test_string():
    sym = SymbolicExecutionEngine("Test/string_single_buffer.ds")
    sym.run()
    string_wanted = "jDcCQ"
    output_buffer = ['[rdi+arg_0]', '[rdi+arg_1]', '[rdi+arg_2]', "[rdi+arg_3]", "[rdi+arg_4]"]
    solution = sym.get_string_solution(output_buffer, string_wanted )
    print str(solution)


if __name__=='__main__':
    test_string()
