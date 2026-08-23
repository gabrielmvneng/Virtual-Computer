class Cpu:
    def __init__(self):
        self.registers = [0, 0, 0, 0, 0]
        self.pc = 0
        self.halted = False
        self.flags = {
            "zero": False,
            "carry": False,
            "negative": False
        }
    def is_imput_valid(self, input1 = 0, input2 = 0):
        if input1 >= len(self.registers) or input2 >= len(self.registers):
            print("ERROR! invalid register index")
            self.halted = True
            return False
        else:
            return True
    def update_flags(self, result, carry):
        self.flags["carry"] = carry
        result %= 256
        self.flags["zero"] = result == 0
        self.flags["negative"] = result & 0b10000000 != 0
        return result

    def execute(self, instruction, memory):
        match instruction:
            case 0x00:
                self.pc += 1
            case 0x01:
                register = memory[self.pc +1]
                value = memory[self.pc +2]
                if self.is_imput_valid(register):
                    self.registers[register] = value
                    self.pc += 3
            case 0x02:
                destination = memory[self.pc +1]
                source = memory[self.pc +2]
                if self.is_imput_valid(destination, source):
                    result = self.registers[destination] + self.registers[source]
                    result = self.update_flags(result, result > 255)
                    self.registers[destination] = result
                    self.pc += 3                    
                
            case 0x03:
                destination = memory[self.pc + 1]
                source = memory[self.pc + 2]

                if self.is_imput_valid(destination, source):
                    a = self.registers[destination]
                    b = self.registers[source]
                    result = a - b
                    result = self.update_flags(result, result <0)
                    self.registers[destination] = result

                    self.pc += 3  
            case 0x04:
                compared = memory[self.pc + 1]
                comparator = memory[self.pc + 2]
                if self.is_imput_valid(compared, comparator):
                    a = self.registers[compared]
                    b = self.registers[comparator]

                    result = a - b
                    self.update_flags(result, result < 0)
                    self.pc += 3  
            case 0x05:
                self.pc = memory[self.pc +1]
            case 0x06:
                if self.flags["zero"] == True:
                    self.pc = memory[self.pc +1]
                else:
                    self.pc +=2
            case 0x07:
                if self.flags["zero"] == True:
                    self.pc += 2
                else:
                    self.pc = memory[self.pc + 1]
            case 0x08:
                register = memory[self.pc + 1]
                local = memory[self.pc +2]
                if self.is_imput_valid(register):
                    self.registers[register] = memory[local]
                    self.pc += 3
            case 0x09:
                register = memory[self.pc + 1]
                local = memory[self.pc + 2]
                if self.is_imput_valid(register):
                    memory[local] = self.registers[register]
                    self.pc += 3
            case 0xFF:
                self.halted = True

memory = [0] * 256
memory[0] = 0x00
memory[1] = 0x01
memory[2] = 0x00
memory[3] = 5
memory[4] = 0x01
memory[5] = 0x01
memory[6] = 0
memory[7] = 0x01
memory[8] = 0x02
memory[9] = 1
memory[10] = 0x03
memory[11] = 0x00
memory[12] = 0x02
memory[13] = 0x04
memory[14] = 0x00
memory[15] = 0x01
memory[16] = 0x07
memory[17] = 0x0a
memory[18] = 0xff
cpu = Cpu()
while not cpu.halted:
    instruction = memory[cpu.pc]
    cpu.execute(instruction, memory)
print(cpu.registers)