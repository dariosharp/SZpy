from imp import reload
from CPUexecution import SymbolicExecutionEngine
import unittest

class Tester_CPU(unittest.TestCase):
    def test_result(self):
        sym = SymbolicExecutionEngine("test_disass.ds", 32)
        sym.run()
        m = sym.get_solution('esi', 1)
        self.assertEqual(str(m), "[arg1 = 1, arg0 = 1749801491]")
        
if __name__=='__main__':
    unittest.main()
