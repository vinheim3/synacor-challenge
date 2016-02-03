#ifndef VM_H
#define VM_H

#include <cstdint>
#include "stack.h"

class VM
{
public:
    VM();
    void load(const char *filename);
    void start();
private:
    void decodeOP();
    uint16_t& mem(uint16_t index);

    uint16_t memory[0x8000];
    uint16_t registers[8];
    Stack stack;
    uint16_t PC;
};

#endif
