
#Introduction
SZpy is based on z3 with Symbolic Execution inspired by [Diary of a reverse-engineer](http://doar-e.github.io/). The aim of this tool is to improve the PoC present in [Breaking Kryptonite's Obfuscation: A Static Analysis Approach Relying on Symbolic Execution](http://goo.gl/FZQJPc). 
There's a simple difference between ZSpy and the PoC: with ZSpy is possible get the input from the output of a particular function.

###When is SZpy useful?
Whenever a function is compiled with static llvm and you're too lazy to analyze it manually.

###How to get SZpy
You need `python2.7` and if you want to use the associated disassembler you need to install [`capstone`](http://www.capstone-engine.org/) python version. Then you can clone SZpy: 
```
$ git clone https://github.com/dariosharp/SZpy.git
```

###Architectures
Now are only supported i386 and x86-64 but will be available in the near future more architectures.

##Execution tutorial
View `EXECUTE.md`.

##Contributors
Myself [dariosharp](https://twitter.com/dariosharp), if you are interested in the project please contact me on twitter or GitHub.
