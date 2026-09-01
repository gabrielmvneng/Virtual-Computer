def parse_register(register):
    if register[0] != "R":
        raise ValueError("Invalid register")
    number = int(register[1:])
    if number < 0 or number > 4:
        raise ValueError("Invalid register")

    return number

def parse_address(target, labels):
    if target in labels:
        address = labels[target]
    else:
        address = int(target)

    if address < 0 or address > 255:
        raise ValueError("Address out of range")

    return address

def assemble_line(line, labels):
    parts = line.replace(',', '').split()
    instruction = parts[0]
    match instruction:
        case "NOP":
            return [0x00]
        case "MOV":
            register = parse_register(parts[1])
            value = int(parts[2])
            if value < 0 or value > 255:
                raise ValueError("Immediate value out of range")
            return [0x01, register, value]
        case "ADD":
            destination = parse_register(parts[1])
            source = parse_register(parts[2])
            return [0x02, destination, source]
        case "SUB":
            destination = parse_register(parts[1])
            source = parse_register(parts[2])
            return [0x03, destination, source]
        case "CMP":
            comparated = parse_register(parts[1])
            comparator = parse_register(parts[2])
            return [0x04, comparated, comparator]
        case "JMP":
            address = parse_address(parts[1], labels)
            return [0x05, address]
        case "JZ":
            address = parse_address(parts[1], labels)
            return [0x06, address]
        case "JNZ":
            address = parse_address(parts[1], labels)
            return [0x07, address]
        case "LOAD":
            register = parse_register(parts[1])
            address_str = parts[2]

            if address_str.startswith('[') and address_str.endswith(']'):
                address_str = address_str[1:-1]
                address = parse_register(address_str)
                return [0x0e, register, address]
            else:
                address = int(address_str)

                if address < 0 or address > 255:
                    raise ValueError("Address out of range")
                return [0x08, register, address]

        case "STORE":
            register = parse_register(parts[1])
            address_str = parts[2]
            
            if address_str.startswith('[') and address_str.endswith(']'):
                address_str = address_str[1:-1]
                address = parse_register(address_str)
                return [0x0f, register, address]
            else:
                address = int(address_str)
            
                if address < 0 or address > 255:
                    raise ValueError("Address out of range")
                return [0x09, register, address]
        case "PUSH":
            register = parse_register(parts[1])
            return [0x0a, register]
        case "POP":
            register = parse_register(parts[1])
            return [0x0b, register]
        case "CALL":
            address = parse_address(parts[1], labels)
            return [0x0c, address]
        case "RET":
            return [0x0d]
        case "END":
            return [0xff]
        case _:
            raise SyntaxError("Invalid OPcode")

def instruction_size(line):
    parts = line.replace(',', '').split()
    instruction = parts[0]

    match instruction:
        case "NOP" | "END" | "RET":
            return 1
        case "JMP" | "JZ" | "JNZ" | "POP" | "PUSH" | "CALL":
            return 2
        case "MOV" | "ADD" | "SUB" | "CMP" | "LOAD" | "STORE":
            return 3
        case _:
            raise ValueError("Invalid opcode")

def find_labels(program):
    labels = {}
    address = 0

    for line in program.splitlines():
        line = line.strip()

        if not line:
            continue
        if ":" in line and not line.endswith(":"):
            raise IndexError("Invalid sintax")
        if line.endswith(":"):
            label = line[:-1]

            if label in labels:
                raise ValueError(f"Duplicate label: {label}")

            labels[label] = address
        else:
            address += instruction_size(line)

    return labels

def assemble(program):
    labels = find_labels(program)
    memory = []

    for line in program.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.endswith(":"):
            continue

        instruction = assemble_line(line, labels)
        memory.extend(instruction)

    return memory

def main():
    with open("program.asm", "r") as file:
        program = file.read()

    memory = assemble(program)

    if len(memory) > 256:
        raise ValueError("Program too large for memory")

    with open("program.bin", "wb") as file:
        file.write(bytes(memory))


if __name__ == "__main__":
    main()