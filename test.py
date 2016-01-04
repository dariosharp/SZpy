from CPUexecution import SymbolicExecutionEngine

import unittest

class TestDisass(unittest.TestCase):
        def test_disassme(self):
            sym = SymbolicExecutionEngine(0x804845A, 0x0804A17C, 0x8048000, "disass/TestDisassembler/adder", 32)
            sym.run()
            m = sym.get_reg_equation_simplified('eax')
            self.assertEqual(str(m), "[arg1 = 3222289541, arg0 = 1072677760]")
unittest.main()

                                            
