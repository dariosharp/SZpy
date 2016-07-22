#!/usr/bin/python2.7 

from imp import reload
from CPUexecution import SymbolicExecutionEngine
from register_convert import *
import unittest


class Tester_CPU(unittest.TestCase):
    def test_number(self):
        sym = SymbolicExecutionEngine("Test/number_test.ds")
        sym.run()
        m = sym.get_solution('esi', 1)
        self.assertEqual(str(m), "[argx4 = 1, argx8 = 1749801491]")

    def test_string(self):
        sym = SymbolicExecutionEngine("Test/string_test.ds")
        sym.run()
        output = ['[rdi+arg_0]', '[rdi+arg_1]', '[rdi+arg_2]']
        m = sym.get_string_solution(output, "@@@")
        self.assertEqual(str(m), '[arg2 = 64, arg1 = 64, arg0 = 64]')

    def test_solveme(self):
        sym = SymbolicExecutionEngine("Test/solveme_edited.ds")
        sym.run()
        output = ['[rdi+arg_0]', '[rdi+arg_1]', '[rdi+arg_2]', "[rdi+arg_3]"]
        m = sym.get_string_solution(output, "e+Lu")
        self.assertEqual(str(m), '[arg1 = 18, arg2 = 35, arg3 = 52, arg0 = 49]')

    def test_string_buffer(self):
        sym = SymbolicExecutionEngine("Test/string_single_buffer.ds")
        sym.run()
        output = ['[rdi+arg_0]', '[rdi+arg_1]', '[rdi+arg_2]', "[rdi+arg_3]", "[rdi+arg_4]"]
        m = sym.get_string_solution(output, "jDcCQ")
        self.assertEqual(str(m), '[arg1 = 34, arg0 = 97, arg2 = 99]')
        
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
