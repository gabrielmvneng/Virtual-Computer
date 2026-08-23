# Virtual-Computer

## CPU

- 5 registers: R0-R4
- Registers: 8-bit
- Memory: 256 bytes
- PC: 8-bit

## Flags

- Z: Zero
- C: Carry
- N: Negative

## Instructions

| Opcode | Instruction | Arguments |
| ------ | ----------- | --------- |
| 00     | NOP         | —         |
| 01     | MOV         | reg, imm  |
| 02     | ADD         | reg, reg  |
| 03     | SUB         | reg, reg  |
| 04     | CMP         | reg, reg  |
| 05     | JMP         | addr      |
| 06     | JZ          | addr      |
| 07     | JNZ         | addr      |
| 08     | LOAD        | reg, addr |
| 09     | STORE       | reg, addr |
| FF     | END         | —         |
