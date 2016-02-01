#!/usr/bin/python2.7 tester_disass.py

from disassembler import *
from imp import reload
import unittest

class TestDisass(unittest.TestCase):
    def test_disassme(self):
        vbase = 0x08048000
        vrip = 0x08048484
        lrip = 0x0804a17c
        dis = Disassembler(vrip, lrip, vbase, 'TestDisassembler/adder', 32)
        with open("TestDisassembler/disassembled.txt") as f:
            for add, mn, op0, op1 in dis.decode():
                string_instruction = "0x{0:x}\t{1}\t{2} {3}\n".format(add, mn, op0, op1)
                correct_instruction = f.readline()
                self.assertEqual(string_instruction, correct_instruction)

    def test_disassme64(self):
        vbase = 0x400000
        vrip = 0x0040078b
        lrip = 0x00400b2f
        dis = Disassembler(vrip, lrip, vbase, 'TestDisassembler/test64', 64)
        with open("TestDisassembler/disassembled64.txt") as f:
            for add, mn, op0, op1 in dis.decode():
                string_instruction = "0x{0:x}\t{1}\t{2} {3}\n".format(add, mn, op0, op1)
                correct_instruction = f.readline()
                self.assertEqual(string_instruction, correct_instruction)

if __name__=="__main__":
    unittest.main()
