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