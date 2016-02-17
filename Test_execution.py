from imp import reload
from CPUexecution import SymbolicExecutionEngine
from register_convert import *

import unittest

class Tester_CPU(unittest.TestCase):
    def test_number(self):
        sym = SymbolicExecutionEngine("Test/number_test.ds")
        sym.run()
        m = sym.get_solution('esi', 1)
        self.assertEqual(str(m), "[arg1 = 1, arg0 = 1749801491]")

    def test_string(self):
        sym = SymbolicExecutionEngine("Test/string_test.ds")
        sym.run()
        # m = sym.get_solution('esi', 1)
        # self.assertEqual(str(m), "[arg1 = 1, arg0 = 1749801491]")
        
    def test_eax(self):
        status = register(r64)
        status['eax'] = 10
        self.assertEqual(status['eax'], 10)
        
    def test_ebx(self):
        status = register(r64)
        status['ebx'] = 10
        self.assertEqual(status['rbx'], 10)

    def test_rcx(self):
        status = register(r64)
        status['rcx'] = 10
        self.assertEqual(status['rcx'], 10)

    def test_rdx(self):
        status = register(r64)
        status['rdx'] = 10
        self.assertEqual(status['edx'], 10)


        
if __name__=='__main__':
    unittest.main()
