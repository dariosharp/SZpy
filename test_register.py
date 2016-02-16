from imp import reload
from register_convert import *
import unittest

class Test_register(unittest.TestCase):
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
