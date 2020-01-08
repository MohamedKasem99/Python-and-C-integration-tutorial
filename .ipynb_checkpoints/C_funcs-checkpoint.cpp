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
double square_root(int i)
{
    return sqrt(i)*10;
}
}