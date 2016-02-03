#include "vm.h"
#include <iostream>
#include <fstream>

VM::VM()
{
    PC = 0;

    for(auto &cell : memory)
        cell = 0;

    for(auto &cell : registers)
        cell = 0;
}

void VM::load(const char *filename)
{
    std::ifstream myfile;
    myfile.open(filename, std::ios::binary | std::ios::ate);

    if (!myfile.is_open())
        throw "Unabled to open file.";

    uint16_t size = myfile.tellg();
    myfile.seekg(0, std::ios::beg);

    char *memblock = new char[size];
    myfile.read(memblock, size);
    myfile.close();

    for(uint16_t i = 0; i < size; i += 2)
    {
        uint8_t byte1 = memblock[i + 1];
        uint8_t byte2 = memblock[i];
        memory[i / 2] = ((byte1 << 8) | byte2);
    }

    delete[] memblock;
}

void VM::start()
{
    while(PC >= 0 & PC <= 32767)
        decodeOP();
    throw "Accessing outside of memory space.";
}

void VM::decodeOP()
{
    switch(memory[PC])
    {
        case 0:
            throw "Halt.";
        case 1:
            mem(PC + 1) = mem(PC + 2);
            PC += 3;
            break;
        case 2:
            stack.push(mem(PC + 1));
            PC += 2;
            break;
        case 3:
            mem(PC + 1) = stack.pop();
            PC += 2;
            break;
        case 4:
            mem(PC + 1) = (mem(PC + 2) == mem(PC + 3));
            PC += 4;
            break;
        case 5:
            mem(PC + 1) = (mem(PC + 2) > mem(PC + 3));
            PC += 4;
            break;
        case 6:
            PC = mem(PC + 1);
            break;
        case 7:
            if (mem(PC + 1) != 0)
                PC = mem(PC + 2);
            else
                PC += 3;
            break;
        case 8:
            if (mem(PC + 1) == 0)
                PC = mem(PC + 2);
            else
                PC += 3;
            break;
        case 9:
            mem(PC + 1) = (mem(PC + 2) + mem(PC + 3)) & 0x7FFF;
            PC += 4;
            break;
        case 10:
            mem(PC + 1) = (mem(PC + 2) * mem(PC + 3)) & 0x7FFF;
            PC += 4;
            break;
        case 11:
            mem(PC + 1) = mem(PC + 2) % mem(PC + 3);
            PC += 4;
            break;
        case 12:
            mem(PC + 1) = mem(PC + 2) & mem(PC + 3);
            PC += 4;
            break;
        case 13:
            mem(PC + 1) = mem(PC + 2) | mem(PC + 3);
            PC += 4;
            break;
        case 14:
            mem(PC + 1) = mem(PC + 2) ^ 0x7FFF;
            PC += 3;
            break;
        case 15:
            mem(PC + 1) = memory[mem(PC + 2)];
            PC += 3;
            break;
        case 16:
            memory[mem(PC + 1)] = mem(PC + 2);
            PC += 3;
            break;
        case 17:
            stack.push(PC + 2);
            PC = mem(PC + 1);
            break;
        case 18:
            PC = stack.pop();
            break;
        case 19:
        {
            uint8_t letter = mem(PC + 1);

            if (letter < 0 | letter > 127)
                throw "Invalid character being printed.";

            std::cout << static_cast<char>(letter);
            PC += 2;
            break;
        }
        case 20:
        {
            uint8_t letter = getchar();
            mem(PC + 1) = letter;
            PC += 2;
            break;
        }
        case 21:
            PC++;
            break;
        default:
            throw memory[PC];
    }
}

uint16_t& VM::mem(uint16_t index)
{
    uint16_t memVal = memory[index];
    if (memVal >= 0 & memVal <= 32767)
        return memory[index];
    else if (memVal >= 32768 & memVal <= 32775)
        return registers[memVal - 32768];
    else
        throw "Invalid memory address.";
}
