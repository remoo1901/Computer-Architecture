"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256

    def ram_read(self, value):
        return self.ram[value]

    def ram_write(self, value, addr):
        self.ram[value] = addr

    def load(self, program):
        """Load a program into memory."""

        address = 0
        with open(program) as file:
            for line in file:
                split_line = line.split("#")[0]
                command = split_line.strip()

                if command == '':
                    continue

                instruction = int(command, 2)
                self.ram_write(address, instruction)

                address += 1

                # print(sys.argv)

                if len(sys.argv) != 2:
                    print("Wrong number of arguments, please pass file name")
                    sys.exit(1)

    """     for instruction in program:
            self.ram[addr] = instruction
            address += 1 """

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010

        isRunning = True
        while isRunning:

            cmd = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if cmd == HLT:
                isRunning = False
                self.pc += 1

            elif cmd == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif cmd == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif cmd == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            else:
                print(f"bad input: {cmd}")
                isRunning = False
