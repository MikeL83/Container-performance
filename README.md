C++ container performance and efficiency
========

This my somewhat small-scale project about comparing C++ sequential containers.
Especially, I'm focusing on std::vector, std::list and std::forward_list and how they
perform in a sequence test. I'm not only measuring execution time but also cache use, 
instructions and ILP (instruction-level parallelism). Nowadays modern CPU chips are so 
powerful with their multiple pipelines and modern ISAs. Therefore, it's curious to see 
how the underlying hardware is being exploited by the compilers. For this test I'm using 
two well-established compilers GCC and CLang (sorry, I don't have a Windows-box available
so I couldn't make the test with Visual C++). The good thing about these two compilers is that
they have full C++14 comformance and the test code heavily uses C++14 features. Also the test
will show if there's any notable differences between these two compilers and their standard 
library implementation. There are many great talks about the subject e.g:

* Chandler Carruth at CppCon 2014 [Efficiency with Algorithms, Performance with Data Structures](https://www.youtube.com/watch?v=fHNmRkzxHWs)
* Chandler Carruth at CppCon 2015 [Tuning C++: Benchmarks, and CPUs, and Compilers! Oh My!](https://www.youtube.com/watch?v=nXaxk27zwlk)
* Chandler Carruth at Meeting C++2015 [Understanding Compiler Optimization](https://www.youtube.com/watch?v=FnGCDLhaxKU)
* Matt Godbolt [x86 Internals for Fun & Profit](https://www.youtube.com/watch?v=hgcNM-6wr34)
* Russell Hadley at Microsoft [The Route to C++ Code Optimization](https://channel9.msdn.com/Shows/Going+Deep/Russell-Hadley-The-Route-to-C-Code-Optimization)
* Eric Brumer at Going Native 2013 [Compiler Confidential](https://channel9.msdn.com/events/GoingNative/2013/Compiler-Confidential)
* Eric Brumer at Build 2013 [Native Code Performance and Memory: The Elephant in the CPU](https://channel9.msdn.com/events/Build/2013/4-329)
* Eric Brumer at Build 2014 [Native Code Performance on Modern CPUs: A Changing Landscape](https://channel9.msdn.com/events/Build/2014/4-587)



I have done the tests in my laptop and it's configuration is as follows:
* Ubuntu 16.04 64 bit
* Intel Core i7-4702MQ CPU 2.20 GHz, for more details about the CPU specs follow the link 	 [Intel](http://ark.intel.com/products/75119)
* System cache sizes:
	L1d cache 32K
	L1i cache 32K
	L2 cache 256K 
	L3 cache 6144K
* GCC 6.2.0/CLang 3.9.0
* Moreover, compiler options -O3 -m64 -std=c++1z -march=corei7-avx -mtune=intel have been used when test codes are compiled.  		

The test code I'm using is so called N sequence test and it consists of three main steps which
are as follows:
	
	1. generate N random number between [1, N]
	2. sort this random number array in ascending order
	3. delete elements from the array one by one in random order until
	   container is empty
	Below is an example output from the program and how it processes different steps:
	
	8 1 4 8 8 9 9 7 2 6
	
	1 2 4 6 7 8 8 8 9 9
	
	1 2 6 7 8 8 8 9 9
	1 2 7 8 8 8 9 9
	1 2 8 8 8 9 9
	1 2 8 8 9 9
	1 2 8 9 9
	1 2 9 9
	1 2 9
	1 2
	2
	
Build
----
Simply type make (assuming you have required compilers otherwise you need modify the Makefile) 

Code	
----
It's easy to use the program. It requires two input arguments number of elements to
process and type of container (list, vector or forward_list).

Example:
	./nsequencebench 1000 vector (C++)

	python3 nsequencebench.py -n 1000 (python3 version)
	
Results
----

--TODO--


License
-------

    Copyright (C) 2016 Mikko Leppänen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

