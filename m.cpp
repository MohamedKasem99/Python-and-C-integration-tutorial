#include <stdio.h>
#include <iostream>
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
int square_root(float i)
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

int main()
{
    double A[] = {1.1, 1.5, 1.5, 1.3, 1.005};
    std::cout<<sum_array(A, 5)<<std::endl;

    square_array(A,5);
    for(int i = 0; i<5; i++)
    {
        std::cout<<A[i]<<"  ";
    }
    std::cout<<std::endl;
    return 0;
}
}