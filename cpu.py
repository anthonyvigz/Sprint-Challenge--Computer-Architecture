"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # self.HLT = 0b00000001
        # self.LDI = 0b10000010
        # self.PRN = 0b01000111
        # self.MUL = 0b10100010
        # self.POP = 0b01000110
        # self.PUSH = 0b01000101
        # self.CALL = 0b01010000
        # self.RET = 0b00010001
        # self.ADD = 0b10100000
        # self.CMP = 0b10100111
        # self.JMP = 0b01010100
        # self.JEQ = 0b01010101
        # self.JNE = 0b01010110
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.flags = 0

        # self.branctable = {}
        # self.branctable[self.HLT] = self.handle_HLT
        # self.branchtable[self.LDI] = self.LDI
        # self.branchtable[self.PRN] = self.handle_PRN
        # self.branchtable[self.MUL] = self.handle_MUL
        # self.branchtable[self.PUSH] = self.handle_PUSH
        # self.branchtable[self.POP] = self.handle_POP
        # self.branchtable[self.CALL] = self.handle_CALL
        # self.branchtable[self.RET] = self.handle_RET
        # self.branchtable[self.ADD] = self.handle_ADD

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print(F"USAGe: {sys.argv[0]} filename")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    num = line.split('#', 1)[0]
                    if num.strip() == '':
                        continue

                    print(num)
                    self.ram[address] = int(num, 2)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = {

        #     # From print8.ls8
        #     0b00000001: self.HLT,
        #     0b10000010l: self.LDI,
        #     0b01000111: self.PRN,
        #     0b10100010: self.MUL,
        #     0b01000110: self.POP
        #     0b01000101: self.PUSH,
        #     0b01010000: self.CALL,
        #     RET = 0b00010001,
        #     ADD = 0b10100000,
        #     CMP = 0b10100111,
        #     JMP = 0b01010100,
        #     JEQ = 0b01010101,
        #     JNE = 0b01010110
        # }

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        # elif op == "SUB": etc
        # elif op == "MUL":
        #     self.reg[reg_a] *= self.reg[reg_b]:
        #         self.flags = 0b0000100
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flags = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flags = 0b0000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flags = 0b0000010
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
        CMD = {
            "HLT":  HLT,
            "LDI": LDI,
            "PRN": PRN,
            "MUL": MUL,
            "POP": POP,
            "PUSH": PUSH,
            "CALL": CALL,
            "RET": RET,
            "ADD": ADD,
            "CMP": CMP,
            "JMP": JMP,
            "JEQ": JEQ,
            "JNE": JNE,
        }

        running = True

        while running:
            register = self.ram[self.pc]
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if register == CMD["LDI"]:
                self.reg[reg_a] = reg_b
                self.pc += 3

            elif register == CMD["HLT"]:
                running = False

            elif register == CMD["PRN"]:
                print(self.reg[reg_a])
                self.pc += 2

            elif register == CMD["MUL"]:
                result = self.alu("MUL", reg_a, reg_b)
                print("MUL", result)
                self.pc += 3

            elif register == CMD["PUSH"]:
                value = self.reg[reg_a]
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = value
                self.pc += 2

            elif register == CMD["POP"]:

                value = self.ram[self.reg[self.sp]]
                self.reg[reg_a] = value
                self.reg[self.sp] += 1
                self.pc += 2

            elif register == CMD["CALL"]:
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = self.pc + 2
                self.pc = self.reg[reg_a]

            elif register == CMD["RET"]:
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1

            elif register == CMD["ADD"]:
                self.reg[reg_a] += self.reg[reg_b]
                self.pc += 3

            elif register == CMD["CMP"]:
                self.alu("CMP", reg_a, reg_b)
                self.pc += 3

            elif register == CMD["JMP"]:
                self.pc = self.reg[reg_a]

            elif register == CMD["JNE"]:
                if self.flags != 0b00000001:
                    self.pc = self.reg[reg_a]
                else:
                    self.pc += 2

            elif register == CMD["JEQ"]:
                if self.flags == 0b00000001:
                    self.pc = self.reg[reg_a]
                else:
                    self.pc += 2

            else:
                sys.exit(1)