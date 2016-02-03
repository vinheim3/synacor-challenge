#ifndef STACK_H
#define STACK_H

#include <cstdint>

class Stack
{
public:
    Stack();
    void push(uint16_t value);
    uint16_t pop();
private:
    struct StackNode
    {
        uint16_t value;
        StackNode *parent;
    } *curr;
};

#endif
