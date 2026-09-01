class Cpu:
    def __init__(self):
        self.registers = [0, 0, 0, 0, 0]
        self.pc = 0
        self.sp = 255
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
                    if local == 0xf0:
                        print(chr(self.registers[register]), end= '')
                    else:
                        memory[local] = self.registers[register]
                    self.pc += 3
            case 0x0a:
                register = memory[self.pc + 1]
                if self.is_imput_valid(register):
                    self.sp -= 1
                    if self.sp < 128:
                        raise OverflowError("Stack overflow")
                    memory[self.sp] = self.registers[register]
                    self.pc += 2
            case 0x0b:
                register = memory[self.pc + 1]
                if self.is_imput_valid(register):
                    if self.sp >= 255:
                        raise OverflowError("Stack underflow")
                    self.registers[register] = memory[self.sp]
                    self.sp += 1
                    self.pc += 2
            case 0x0c:
                address = memory[self.pc + 1]
                return_address = self.pc + 2
                self.sp -= 1
                if self.sp < 128:
                    raise OverflowError("Stack overflow")
                memory[self.sp] = return_address
                self.pc = address
            case 0x0d:
                self.pc = memory[self.sp]
                self.sp += 1
                if self.sp > 255:
                    raise OverflowError("Stack underflow")
            case 0x0e:
                register = memory[self.pc + 1]
                local = memory[self.pc +2]
                if self.is_imput_valid(register, local):
                    self.registers[register] = memory[self.registers[local]]
                    self.pc += 3
            case 0x0f:
                register = memory[self.pc + 1]
                local = memory[self.pc + 2]
                if self.is_imput_valid(register, local):
                    if self.registers[local] == 0xf0:
                        print(chr(self.registers[register]), end= '')
                    else:
                        memory[self.registers[local]] = self.registers[register]
                    self.pc += 3
            case 0xFF:
                self.halted = True

def load_program(filename):
    with open(filename, "rb") as file:
        program = list(file.read())

    if len(program) > 256:
        raise ValueError("Program too large for memory")

    memory = [0] * 256
    memory[:len(program)] = program

    return memory

memory = load_program("program.bin")

cpu = Cpu()
while not cpu.halted:
    instruction = memory[cpu.pc]
    cpu.execute(instruction, memory)