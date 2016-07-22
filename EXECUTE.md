##Example of challs:
  I want to resolve this challs called solveme.c:
  ```
#include <stdio.h>
#include <string.h>

char *manipolation(char * s){
  s[0] = s[0] + s[3];
  s[1] = (s[1] * 8) - s[0];
  s[2] = (s[1] | s[0]) & (~s[2]);
  s[3] = (s[3] >> 1) + s[0] - (s[1]>>2);
  return s;
}

int main(int argc, char *argv[])
{
  if(argc!=2)
  {
    printf("Run as ./example 'string'\n");
    return 1;
  }
  if(strlen(argv[1])!=4)
  {
    printf("4 chars len pls\n");
    return 1;    
  }
  printf("You can only win with 'e+Lu' as a solution\n");
  char *p = manipolation(argv[1]);
  if(strcmp(p, "e+Lu")==0)
  {
      printf("Good solution!\n");
      return 0;
  }  
  printf("retry..\n");
  return 0;
}
  ```
  
  If you compile C code with `clang solveme.c -o solveme` (you can find the compiled C file in SZpy/disass/TestDisassembler/solveme) and disassembly it you will see that the function `manipolation` will be very boring to reverse. Therefore It's necessary use SZpy.
  
##How to start
  It's fondamental to find the start and end address of function that you want to solve. In the solveme the `manipolation` function starts on 0x004005d0 and end on 0x00400667.
  Ok now It's possible create a file containing the disassembly of this function. Lets do it with included disassembler:
  ```
#!/usr/bin/python2.7 disassSolveme.py

from disass.disassembler import *
from imp import reload

def dis():
    vbase = 0x00400000
    start = 0x004005d0
    end = 0x00400667
    dis = Disassembler(start, end, vbase, 'disass/TestDisassembler/solveme', 64)
    dis.store_istruction("Test/solveme.ds")

if __name__=="__main__":
    dis()
    print "done"

  ```
  
##Fix the disassembled
It's common remove unnecessary instructions like `push rbp; mov rbp rsp;` and `pop rbp;`.
SZpy sometimes automatically understands where is the location of the strings that you want solve, but sometimes it need your help. 
SZpy looks in `mov` where the source location is not setted, like `mov rdi [rbp+arg_x8]` if `[rbp+arg_x8]` not setted before.
For solveme.ds is only necessary remove `push rbp; mov rbp rsp;` and `pop rbp;` and rename it in SZpy/Test/solveme_edited.ds. 

##Lets start the automatic resolver
```
from imp import reload
from CPUexecution import SymbolicExecutionEngine


def test_string():
    sym = SymbolicExecutionEngine("Test/solveme_edited.ds")
    sym.run()
    string_wanted = "e+Lu"
    output_buffer = ['[rdi+arg_0]', '[rdi+arg_1]', '[rdi+arg_2]', "[rdi+arg_3]"]
    solution = sym.get_string_solution(output_buffer, string_wanted )
    print str(solution)


if __name__=='__main__':
    test_string()
```
The solution of your problem is:
```
[arg3 = 35, arg1 = 52, arg0 = 49, arg2 = 18]
```
If you try `./solveme $(perl -e 'print "\x31\x12\x23\x34"'` you will get the correct solution!

Awesome I know. Enjoy it. 
