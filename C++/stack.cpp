#include "stack.h"

Stack::Stack()
{
    curr = nullptr;
}

void Stack::push(uint16_t value)
{
    if (curr == nullptr)
    {
        curr = new StackNode {value, nullptr};
    }
    else
    {
        curr = new StackNode {value, curr};
    }
}

uint16_t Stack::pop()
{
    if (curr == nullptr)
    {
        throw "Popping from empty stack.";
    }
    else
    {
        int val = curr->value;
        StackNode *top = curr->parent;
        delete curr;
        curr = top;
        return val;
    }
}
