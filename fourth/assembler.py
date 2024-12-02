import sys
import csv

def parse_instruction(line):
    parts = line.strip().split()
    command = parts[0]
    args = list(map(int, parts[1:]))
    return command, args

def assemble(instructions):
    binary_data = []
    log_data = []
    
    for instruction in instructions:
        cmd, args = parse_instruction(instruction)
        
        if cmd == 'LOAD_CONST':
            A, B, C = args
            binary_data.append(0xE9)  # Команда LOAD_CONST
            binary_data += [A, B, C, 0, 0]  # Заполняем данные
        
        elif cmd == 'READ_MEM':
            A, B, C = args
            binary_data.append(0xA7)  # Команда READ_MEM
            binary_data += [A, B, C, 0, 0]  # Заполняем данные
            
        elif cmd == 'WRITE_MEM':
            A, B, C, D = args
            binary_data.append(0xC1)  # Команда WRITE_MEM
            binary_data += [A, B, C, D, 0]  # Заполняем данные
            
        elif cmd == 'BITWISE_CIRCULAR_RIGHT':
            A, B, C = args
            binary_data.append(0x1B)  # Команда BITWISE_CIRCULAR_RIGHT
            binary_data += [A, B, C, 0, 0]  # Заполняем данные
        
        # Логирование
        log_data.append(f'{cmd}={args}')
    
    return binary_data, log_data

def write_binary_file(data, path):
    with open(path, 'wb') as f:
        f.write(bytes(data))

def write_log_file(log_data, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        for log in log_data:
            writer.writerow([log])
            
            # buffer = str(log)
            # buffer = buffer.replace('=', ' ')
            # buffer = buffer.replace('[', ' ')
            # buffer = buffer.replace(']', ' ')
            # buffer = buffer.replace(',', ' ')
            # buffer = buffer.split()
            # print(buffer)
            # temp = ""
            # for i in buffer:
            #     temp += (str(i) + ', ')
            # writer.writerow([temp])

def main():
    if len(sys.argv) < 4:
        print("Usage: assembler.py <input_file> <output_file> <log_file>")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    
    with open(input_file, 'r') as f:
        instructions = f.readlines()
    
    binary_data, log_data = assemble(instructions)
    
    write_binary_file(binary_data, output_file)
    write_log_file(log_data, log_file)

if __name__ == "__main__":
    main()
