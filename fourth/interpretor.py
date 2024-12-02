import sys
import csv

class VM:
    def __init__(self):
        self.memory = [0] * 256  # Память виртуальной машины
        self.registers = [0] * 16  # Регистры

    def load_instruction(self, instruction):
        opcode = instruction[0]
        if opcode == 0xE9:  # LOAD_CONST
            A, B, C = instruction[1:4]  # Извлекаем только необходимые параметры
            self.registers[B] = C
        
        elif opcode == 0xA7:  # READ_MEM
            A, B, C = instruction[1:4]
            addr = self.registers[C]
            if 0 <= addr < len(self.memory):  # Проверка диапазона
                self.registers[B] = self.memory[addr]
        
        elif opcode == 0xC1:  # WRITE_MEM
            A, B, C, D = instruction[1:5]
            addr = self.registers[C] + A
            if 0 <= addr < len(self.memory):  # Проверка диапазона
                self.memory[addr] = self.registers[D]
        
        elif opcode == 0x1B:  # BITWISE_CIRCULAR_RIGHT
            A, B, C = instruction[1:4]
            if 0 <= self.registers[B] < len(self.memory):  # Проверка диапазона
                value = self.memory[self.registers[B]]
                self.memory[self.registers[B]] = (value >> 1) | ((value & 1) << 7)  # Циклический сдвиг вправо

def main():
    if len(sys.argv) < 4:
        print("Usage: interpreter.py <binary_file> <output_file> <memory_range>")
        return
    
    binary_file = sys.argv[1]
    output_file = sys.argv[2]
    memory_range = int(sys.argv[3])
    
    vm = VM()
    
    with open(binary_file, 'rb') as f:
        while byte := f.read(5):
            instruction = list(byte)
            instruction[0] = instruction[0]  # Убедимся, что первый байт остается в формате opcodes
            vm.load_instruction(instruction)
    
    # Сохраняем результаты в CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(min(memory_range, len(vm.memory))):  # Проверка диапазона
            writer.writerow([i, vm.memory[i]])

if __name__ == "__main__":
    main()
