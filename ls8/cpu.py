"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0 # program counter,address of the currently executing instruction
        self.fl = 0 # holds the current flags status
        #Commands
        self.HLT = 0b00000001 # aka HALT, exit the emulator
        self.LDI = 0b10000010 # aka LOAD, sets a value to a specified register.
        self.PRN = 0b01000111 # aka PRINT, prints value of a register
    # should accept the address to read and return the value stored there.
    def ram_read(self, index):
        return self.ram[index]
    # should accept a value to write, and the address to write it to.
    def ram_write(self, value, index):
        self.ram[index] = value
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            # read memory at pc, set to instruction register
            # this is the same as the memory[pc] array [PRINT_TIM, PRINT_TIM, HALT]
            ir = self.ram_read(self.pc)
        # look at the following 1 or 2 bytes of memory, stored as variables..why exactly??
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # if command = LDI
            if ir == self.LDI:
                #grab the memory address 1 past the command, here the value is the spot in ram to save the value
                #   = memory[pc + 1]
                reg_index = self.ram[self.pc + 1]
                # Grab value 2 pass the command, this value will get stored in the ram slot above
                value_to_save = self.ram[self.pc + 2]
                self.registers[reg_index] = value_to_save
                # increment program counter enough to pass the command + the slot + the value
                self.pc +=2
            if ir == self.PRN:
                reg_index = self.ram[self.pc+1]
                print(self.registers[reg_index])
                self.pc +=1
            if ir == self.HLT:
                running = False

            self.pc +=1