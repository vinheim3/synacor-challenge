#ifndef STACK_H
#define STACK_H

template <typename T>
class Stack
{
public:
    Stack()
    {
        curr = nullptr;
    }

    void push(T value)
    {
        curr = new StackNode {value, curr};
    }

    T pop()
    {
        if (curr == nullptr)
            throw "Popping from empty stack.";
        
        T val = curr->value;
        StackNode *top = curr->parent;
        delete curr;
        curr = top;
        return val;
    }
private:
    struct StackNode
    {
        T value;
        StackNode *parent;
    } *curr;
};

#endif
