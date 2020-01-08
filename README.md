# Calling compiled C code with python

This tutorial explores how to compile C code and importing it to your scope. I will be using linux (ubuntu 18.04), but it will work with whatever OS    
**You have to have a c/c++ compiler installed**  
#### 1- Create a C File "C_funcs.cpp" with some functions (squre and cube in our case). Something like this:  
```c++
#include <stdio.h>
#include <math.h>
extern "C"
{
    int square(int i) {
        return i * i;
    }
    int cube(int i)
    {
        return i * i * i;
    }
    float square_root(float i)
    {
        return sqrt(i);
    }

    double sum_array(double a[], int size_a)
    {
        double summ = 0;
        for(int i = 0; i<size_a; i++)
        {
            summ += a[i];
        }
        return summ;
    }
    void square_array(double a[], int size_a)
    {
        for(int i = 0; i<size_a; i++)
        {
            a[i] *= a[i];
        }
    }
}
```
***It's VERY important to use the ```extern "C"``` syntax because c++ has many***
#### 2- Place the .cpp/.c file in the same directory in which you have your python code.  
#### 3- Compile this file to a shared library with the following command:  
```bash
gcc -shared -o C_funcs.o C_funcs.cpp
```
since we included the ```extern "C"``` syntax, the compiler is basically changing c++ into c and then using the compiled c code with python.
#### 4- run the following python code to test it for yourself.  
***I use python os library to get to the .o file directory***


```python
from ctypes import *
import os
import numpy as np
import time
```


```python
!g++ -fPIC -shared -o C_funcs.so C_funcs.cpp
```


```python
crnt_work_dir = os.getcwd()

for file_name in os.listdir(crnt_work_dir):
    #find the file with the .o extension
    if file_name.endswith(".so"):
        #create full dir string
        o_file = os.path.join(crnt_work_dir,file_name)

```

### Set argument types and return type
It is very important to set these parameters for the python to be able to communicate them to the C compiled code. Python does not cast variables to their appropriate data types by default, so it has to be explicitely set for every function. Both arguments and return types have to be speciefied once


```python
#get object file in scope
my_funcs = CDLL(o_file)

#set argument types (in order)
my_funcs.square.argtypes = [c_int]
my_funcs.cube.argtypes = [c_int]
my_funcs.square_root.argtypes = [c_float]
my_funcs.sum_array.argtypes = [POINTER(c_double), c_int]
my_funcs.square_array.argtypes = [POINTER(c_double), c_int]

#set return type
my_funcs.square.restype = c_int
my_funcs.cube.restype = c_int
my_funcs.square_root.restype = c_float
my_funcs.sum_array.restype = c_double
my_funcs.square_array.restype = c_void_p

```

### Testing basic functions


```python
rands = [1.1, 1.5, 1.5, 1.3, 1.005]
size = 5

A = c_double * size
Arr = A(*rands)


print(f'square(4): {my_funcs.square(4)}')
print(f'cube(4): {my_funcs.cube(4)}')
print(f'square_root(20.5): {my_funcs.square_root(20.5)}')
print(f'sum_array{rands}: {my_funcs.sum_array(Arr,size)}')
```

    square(4): 16
    cube(4): 64
    square_root(20.5): 4.527692794799805
    sum_array[1.1, 1.5, 1.5, 1.3, 1.005]: 6.404999999999999


### comparing speed up advantages of C over python
When working with arrays, the number of computations grows noticeably and this is where C has a great advantage because it doesn't have to check for types every time.


```python
size_arr = 10000000
huge_arr = (np.random.randn(size_arr))
c_arr = (c_double * size_arr)(*huge_arr)


t1 = time.time()
x1 = sum(huge_arr)
elapsed_1 = time.time() - t1 
print('it takes python {} ms to sum'.format(elapsed_1))

t2 = time.time()
x2 = my_funcs.sum_array(c_arr,size_arr)
elapsed_2 = time.time() - t2 
print('it takes C {} ms to sum'.format(elapsed_2))

t3 = time.time()
x3 = huge_arr.sum()
elapsed_3 = time.time() - t1 
print('it takes numpy {} ms to sum'.format(elapsed_3))

print(f'\n\nSpeedup:{elapsed_1/elapsed_2}\nError: {x1 - x2}')
```

    it takes python 1.9072742462158203 ms to sum
    it takes C 0.034125328063964844 ms to sum
    it takes numpy 1.9473395347595215 ms to sum
    
    
    Speedup:55.8902830953246
    Error: 0.0


### Testing pass by reference for multiple input and multiple outputs
Using arrays with void return


```python
before_square = [1,2,3,4,5]
for_square = (c_double * len(before_square))(*before_square)
my_funcs.square_array(for_square, len(before_square))

for i in for_square:
    print(i, end='  ')
```

    1.0  4.0  9.0  16.0  25.0  
