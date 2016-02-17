
allreg = [ 'rax', 'rbx', 'rcx','rdx','rsi','rdi', 'rbp', 'rsp', 'rip', 'r8',
           'r9' , 'r10', 'r11', 'r12', 'r13', 'r14', 'r15', 'eax', 'ebx',
           'ecx','edx','esi','edi', 'ebp', 'esp', 'eip', 'r8d', 'r9d' , 'r10d',
           'r11d', 'r12d', 'r13d', 'r14d', 'r15d', 'ax', 'bx', 'cx','dx','sp',
           'bp', 'si', 'di',  'r8w', 'r9w' , 'r10w', 'r11w', 'r12w', 'r13w',
           'r14w', 'r15w', 'al', 'bl', 'cl', 'dl', 'sil','dil', 'spl', 'bpl',
           'r8b', 'r9b' , 'r10b', 'r11b', 'r12b', 'r13b', 'r14b', 'r15b']



r64 = {
    'rax' : None,
    'rbx' : None,
    'rcx' : None,
    'rdx' : None,
    'rsi' : None,
    'rdi' : None,
    'rbp' : None,
    'rsp' : None,
    'rip' : None,
    'r8'  : None,
    'r9'  : None,
    'r10' : None,
    'r11' : None,
    'r12' : None,
    'r13' : None,
    'r14' : None,
    'r15' : None
}


r32 = {
    'eax' : 'rax',
    'ebx' : 'rbx',
    'ecx' : 'rcx',
    'edx' : 'rdx',
    'esi' : 'rsi',
    'edi' : 'rdi',
    'ebp' : 'rbp',
    'esp' : 'rsp',
    'eip' : 'rip',
    'r8d'  : 'r8',
    'r9d'  : 'r9',
    'r10d' : 'r10', 
    'r11d' : 'r11',
    'r12d' : 'r12',
    'r13d' : 'r13',
    'r14d' : 'r14',
    'r15d' : 'r15'
}

r16 = {
    'ax' : 'rax',
    'bx' : 'rbx',
    'cx' : 'rcx',
    'dx' : 'rdx',
    'sp' : 'rsp',
    'bp' : 'rbp',
    'si' : 'rsi',
    'di' : 'rdi',
    'r8w'  : 'r8',
    'r9w'  : 'r9',
    'r10w' : 'r10',
    'r11w' : 'r11',
    'r12w' : 'r12',
    'r13w' : 'r13',
    'r14w' : 'r14', 
    'r15w' : 'r15'
}

r8 = {
    'al' : 'rax',
    'bl' : 'rbx',
    'cl' : 'rcx',
    'dl' : 'rdx',
    'sil' : 'rsi',
    'dil' : 'rdi',
    'spl' : 'rsp',
    'bpl' : 'rbp',
    'r8b'  : 'r8',
    'r9b'  : 'r9',
    'r10b' : 'r10',
    'r11b' : 'r11',
    'r12b' : 'r12',
    'r13b' : 'r13',
    'r14b' : 'r14',
    'r15b' : 'r15'
}



class register:
    def __init__(self, r):
        self._r = r
        
    def __setitem__(self, key, value):
        key, value = (key in r32 and self.set32(key, value)) or \
                     (key in r16 and self.set16(key, value)) or \
                     (key in r8 and self.set8(key, value)) or (key, value)
        self._r[key] = value
        
    def __getitem__(self, key):
        return (key in r64 and self._r[key]) or \
            (key in r32 and self.get32(key)) or \
            (key in r16 and self.get16(key)) or \
            (key in r8 and self.get8(key)) 

    
    def set32(self, key, value):
        value += (self._r[r32[key]] != None and
                  self._r[r32[key]] & 0xFFFFFFFF00000000) or 0
        return (r32[key], value)
    
    def get32(self, key):
        return (self._r[r32[key]] != None \
                and self._r[r32[key]] & 0xFFFFFFFF) or None 

    def set16(self, key, value):
        value += (self._r[r16[key]] != None and
                  self._r[r16[key]] & 0xFFFFFFFFFFFF0000) or 0
        return key, value
    
    def get16(self, key):
        return (self._r[r16[key]] != None
                and self._r[r16[key]] & 0xFFFF) or None 

    def set8(self, key, value):
        value += (self._r[r8[key]] != None and
                  self._r[r8[key]] & 0xFFFFFFFFFFFFFF00) or 0
        return key, value
    
    def get8(self, key):
        return (self._r[r8[key]] != None
                and self._r[r8[key]] & 0xFF) or None 
