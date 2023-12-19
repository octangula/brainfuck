# small brainfuck interpreter
# rika // python 3.10.7

import sys, os

memory = [0 for i in range(30000)] # initialize with 30000 memory cells
pointer = 0 # initialize pointer at 0
output = ""

if len(sys.argv) != 2:
    print("usage: py bf.py <file.bf>")
    quit()

with open(sys.argv[1], "r") as f:
    program = "".join(char for char in f.read() if char in "<>+-[].,") # cut anything not used in brainfuck

loops = [] 
mappings = {}
for i in range(len(program)): # map loops to dicts for easy loop control
    if program[i] == "[":
        loops.append(i)
    if program[i] == "]":
        mappings[i] = loops[-1]
        mappings[loops[-1]] = i
        loops.pop(-1)

i = 0
while i < len(program):
    c = program[i]

    # move pointer 1 to the left
    if c == "<":
        pointer = (pointer - 1) % len(memory)

    # move pointer 1 to the right
    if c == ">":
        pointer = (pointer + 1) % len(memory)

    # add 1 to pointer(mod 256 for underflow/overlow)
    if c == "+":
        memory[pointer] = (memory[pointer] + 1) % 256

    # subtract 1 from pointer(mod 256 for underflow/overflow)
    if c == "-":
        memory[pointer] = (memory[pointer] - 1) % 256

    # clear screen, convert pointer to ascii and output
    if c == ".":
        output += chr(memory[pointer])
        os.system("cls")
        print(output)

    # take input and convert from ascii to int
    if c == ",":
        memory[pointer] = ord(input())

    # if the pointer is on a 0, skip the loop and jump to the matching ]
    if c == "[":
        if memory[pointer] == 0:
            i = mappings[i]

    # if the pointer is NOT on a 0, continue the loop by jumping back to the matching [
    if c == "]":
        if memory[pointer] != 0:
            i = mappings[i]
            
    i += 1
