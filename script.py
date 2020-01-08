from ctypes import *
import os
import numpy as np
import time

crnt_work_dir = os.getcwd()
## run this linux command in your current directory to compile your .cpp file into a shared library 
## g++ -fPIC -shared -o C_funcs.so [FILE_NAME]
## This code will look for the file.so and use it for the rest of this script.
for file_name in os.listdir(crnt_work_dir):
    #find the file with the .o extension
    if file_name.endswith(".so"):
        #create full dir string
        o_file = os.path.join(crnt_work_dir,file_name)


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


# testing all basic functions
rands = [1.1, 1.5, 1.5, 1.3, 1.005]
size = 5

A = c_double * size
Arr = A(*rands)


print(f'square(4): {my_funcs.square(4)}')
print(f'cube(4): {my_funcs.cube(4)}')
print(f'square_root(20.5): {my_funcs.square_root(20.5)}')
print(f'sum_array{rands}: {my_funcs.sum_array(Arr,size)}')



#comparing speed up advantages of C over python
#and working with arrays

size_arr = 10000
huge_arr = list(np.random.randn(size_arr))
c_arr = (c_double * size_arr)(*huge_arr)


t1 = time.time()
x1 = sum(huge_arr)
elapsed_1 = time.time() - t1 
print('it takes python {} ms to sum'.format(elapsed_1))

t2 = time.time()
x2 = my_funcs.sum_array(c_arr,size_arr)
elapsed_2 = time.time() - t2 
print('it takes python {} ms to sum'.format(elapsed_2))
print(f'\n\nSpeedup:{elapsed_1/elapsed_2}\nError: {x1 - x2}')



# Testing pass by reference for multiple input and multiple outputs
# Using arrays with void return

before_square = [1,2,3,4,5]
for_square = (c_double * len(before_square))(*before_square)
my_funcs.square_array(for_square, len(before_square))

for i in for_square:
    print(i, end='  ')