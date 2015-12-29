#!/usr/bin/python2.7 tester_disass.py

from disassembler import *
from imp import reload
import unittest


class TestDisass(unittest.TestCase):
    def test_disassme(self):
        vbase = 0x08048000
        vrip = 0x08048484
        lrip = 0x0804a17c
        dis = Disassembler(vrip, lrip, vbase, '../adder', 32)
        with open("disassembled.txt") as f:
            for add, mn, op0, op1 in dis.decode():
                string_instruction = "0x{0:x}\t{1}\t{2}, {3}\n".format(add, mn, op0, op1)
                correct_instruction = f.readline()
                self.assertEqual(string_instruction, correct_instruction)
            
unittest.main()
