"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU.
        Add list properties to the `CPU` class to hold 256 bytes of memory and 8
        general-purpose registers.
        """
        self.reg = [0] * 8  # register
        self.ram = [0] * 256  # changed ram from 8 to 256  / location in memory
        self.pc = 0  # Program Counter, address of the currently executing instruction
        self.ir = None  # Instruction Register, contains a copy of the currently executing instruction
        self.branchtable = {}  # from load() previously
        self.branchtable[0b00000001] = self.handle_HLT
        self.branchtable[0b10000010] = self.handle_LDI
        self.branchtable[0b01000111] = self.handle_PRN
        # self.branchtable[0b10100010] = self.handle_MUL
        self.branchtable[0b10100111] = self.handle_CMP
        self.branchtable[0b01010100] = self.handle_JMP
        self.branchtable[0b01010101] = self.handle_JEQ
        self.branchtable[0b01010110] = self.handle_JNE

    def load(self, filename):
        """Load a program into memory."""

        address = 0  # DO NOT TRY 1 or 2 haha

        with open(filename) as f:
            for line in f:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                # print("NUM", num)  # some zeros and ones
                if num == "":
                    continue  # continue even if blank
                value = int(num, 2)
                # print("VAL!!", value)  # pretty cool stuff
                self.ram[address] = value
                # print("RAM ADDRESS", address)
                address += 1  # iterates

        # For now, we've just hardcoded a program:

#         program = [
#             # From print8.ls8
#             0b10000010, # LDI R0,8
#             0b00000000, #_operands_ represents R0
#             0b00001000, #_operands_ represents value
#             0b01000111, # PRN R0
#             0b00000000, #_operands_ represents R0
#             0b00000001, # HLT
#         ]

    def ram_read(self, address):
        """
        should accept the address to read and return the value stored there.
        """
        return self.ram[address]

    def ram_write(self, value, address):
        """should accept a value to write, and the address to write it to."""
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # ADD CMP CONDITIONAL / Flag
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            # if equal set = flag
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100
            # If reg_a is less than reg_b, set `L` flag to 1,
            # otherwise set it to 0
            if self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            # If reg_a is greater than reg_b, set `G` flag
            # to 1 otherwise set it to 0.
        else:
            raise Exception("Unsupported ALU operation")
            # sorted in handle functions below

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

    def handle_HLT(self):
        self.pc = 0
        return 'HLT'
        # halt / exit

    def handle_LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3
        # load/store value in register

    def handle_PRN(self):
        index = self.ram_read(self.ram[self.pc] + 1)
        print(self.reg[index])
        self.pc += 2
        # Print value in register

    def handle_CMP(self):
        register_a = self.ram_read(self.pc + 1)
        register_b = self.ram_read(self.pc + 2)
        self.alu("CMP", register_a, register_b)
        self.pc += 3

    def handle_JMP(self):
        address = self.ram_read(self.pc + 1)
        self.pc = self.reg[address]
        # JMP register to the address stored in the given register.
        # Set the PC to the address stored in the given register.

    def handle_JEQ(self):  # EQUAL
        address = self.ram_read(self.pc + 1)
        if self.flag == 0b00000001:
            self.pc = self.reg[address]
        else:
            self.pc += 2
        # set flag if = is true / jumps

    def handle_JNE(self):  # NOT EQUAL
        address = self.ram_read(self.pc + 1)
        if self.flag != 0b00000001:
            self.pc = self.reg[address]
        else:
            self.pc += 2
        # set flag if = is false or 0 / jumps

    def run(self):
        """Run the CPU.
        """

        running = True
        while running:
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            IR = self.ram_read(self.pc)
            HLT = self.handle_HLT
            # LDI = self.handle_LDI
            # PRN = self.handle_PRN
            # MUL = self.handle_MUL

            try:
                return_command = self.branchtable[IR]()
                if return_command == 'HLT':
                    running = False
            except KeyError:
                print(f'Error: Unknow command: {IR}')
                sys.exit(1)


cpu = CPU()
print(sys.argv[1])
cpu.load(sys.argv[1])
cpu.run()
