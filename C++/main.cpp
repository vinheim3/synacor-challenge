#include "vm.h"
#include <iostream>

int main()
{
    VM vm;
    vm.load("challenge.bin");

    try
    {
        vm.start();
    }
    catch (const char* e)
    {
        std::cout << "Error: " << e;
    }
    catch (unsigned short e)
    {
        std::cout << "Error: " << e;
    }

    return 0;
}
