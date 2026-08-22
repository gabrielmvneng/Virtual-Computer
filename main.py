class Cpu:
    def __init__(self):
        self.registers = [0, 0, 0, 0, 0]
        self.pc = 0
        self.halted = False

    def execute(self, instruction, memory):
        arg1 = memory[self.pc +1]
        arg2 = memory[self.pc +2]
        match instruction:
            case 0x00:
                self.pc += 1
            case 0x01:
                if arg1 >= len(self.registers):
                    print("ERROR! invalid register index")
                    self.halted = True
                else:
                    self.registers[arg1] = arg2
                    self.pc += 3
            case 0x02:
                if arg1 >= len(self.registers) or arg2 >= len(self.registers):
                    print("ERROR! invalid register index")
                    self.halted = True
                else:
                    self.registers[arg1] = self.registers[arg1] + self.registers[arg2]
                    self.pc +=3
                
            case 0x03:
                if arg1 >= len(self.registers) or arg2 >= len(self.registers):
                    print("ERROR! invalid register index")
                    self.halted = True
                else:
                    self.registers[arg1] = self.registers[arg1] - self.registers[arg2]
                    self.pc +=3
            case 0xFF:
                self.halted = True

memory = [0] * 256
memory[0] = 0x00
memory[1] = 0x01
memory[2] = 0x00
memory[3] = 45
memory[4] = 0xFF
cpu = Cpu()
while not cpu.halted:
    instruction = memory[cpu.pc]
    cpu.execute(instruction, memory)
print(cpu.registers)