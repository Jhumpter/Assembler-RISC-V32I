global labels
labels = {}

def reg_translator(reg):
    #Traduz o registrador (ou máscara) para o número correspondente
    translator = ["zero","ra","sp","gp","tp","t0","t1","t2",
     "s0","s1","a0","a1","a2","a3","a4","a5",
     "a6","a7","s2","s3","s4","s5","s6",
     "s7","s8","s9","s10","s11","t3",
     "t4","t5","t6"]
    if reg in translator:
        return to_bin(translator.index(reg), 5)
    elif reg[0] == "x" and reg[1:].isdigit() and 0 <= int(reg[1:]) <= 31:
        return to_bin(int(reg[1:]), 5)
    elif reg == "fp":
        return to_bin(8, 5)
    else:        
        raise ValueError("Invalid register name: " + reg)

def to_hex(inst, digits=8):
    #Passa o número binário para hexadecimal com digits dígitos
    return "0x"+hex(int(inst, 2))[2:].zfill(digits)

def to_bin(num, bits):
    #Calcula o complemento de 2 para números negativos e retorna a representação binária de num com o número de bits especificado
    if num >=0:
        return bin(num)[2:].zfill(bits)
    elif num < 0:
        return bin((1 << bits) + num)[2:]
    else:
        raise ValueError("Invalid number: " + str(num))

def label_adress(label):
    #Retorna o endereço de uma label
    for key in labels:
        if key == label:
            return labels[key]
    raise ValueError("Label not found: " + label)

def r_inst (type, res, arg1, arg2):
    #funct7/rs2/rs1/funct3/rd/opcode
    arg1 = reg_translator(arg1)
    arg2 = reg_translator(arg2)
    res = reg_translator(res)
    if type == "add":
        return to_hex("0000000"+arg2+arg1+"000"+res+"0110011")
    elif type == "sub":
        return to_hex("0100000"+arg2+arg1+"000"+res+"0110011")
    elif type == "and":
        return to_hex("0000000"+arg2+arg1+"111"+res+"0110011")
    elif type == "or":
        return to_hex("0000000"+arg2+arg1+"110"+res+"0110011")
    elif type == "xor":
        return to_hex("0000000"+arg2+arg1+"100"+res+"0110011")
    elif type == "slt":
        return to_hex("0000000"+arg2+arg1+"010"+res+"0110011")
    elif type == "sll":
        return to_hex("0000000"+arg2+arg1+"001"+res+"0110011")
    elif type == "srl":
        return to_hex("0000000"+arg2+arg1+"101"+res+"0110011")

def i_inst (type, res, arg1, imm):
    #imm[11:0]/rs1/funct3/rd/opcode
    if type == "lw" or type == "lhu":
        arg1, imm = imm, arg1
        arg1 = reg_translator(arg1)
        imm = to_bin(int(imm), 12)
    else:
        arg1 = reg_translator(arg1)
        imm = to_bin(int(imm), 12)
    res = reg_translator(res) 
    if type == "lw":
        return to_hex(imm+arg1+"010"+res+"0000011")
    elif type == "addi":
        return to_hex(imm+arg1+"000"+res+"0010011")
    elif type == "jalr":
        return to_hex(imm+arg1+"000"+res+"1100111")
    elif type == "slti":
        return to_hex(imm+arg1+"010"+res+"0010011")
    elif type == "andi":
        return to_hex(imm+arg1+"111"+res+"0010011")
    elif type == "ori":
        return to_hex(imm+arg1+"110"+res+"0010011")
    elif type == "xori":
        return to_hex(imm+arg1+"100"+res+"0010011")
    elif type == "lhu":
        return to_hex(imm+arg1+"101"+res+"0000011")

def s_inst (type, arg2, imm, arg1):
    #imm[11:5]/rs2/rs1/funct3/imm[4:0]/opcode
    imm = to_bin(int(imm,0), 12)
    arg1 = reg_translator(arg1)
    arg2 = reg_translator(arg2)
    if type == "sw":
        return to_hex(imm[:7]+arg2+arg1+"010"+imm[7:]+"0100011")

def j_inst (type, res, imm, line_num):
    #imm[20|10:1|11|19:12]/rd/opcode
    res = reg_translator(res)
    try:
        imm = to_bin(int(imm,0), 21)
    except ValueError:
        imm = (label_adress(imm) - line_num)*4
        imm = to_bin(imm, 21)
    if type == "jal":
        return to_hex(imm[0]+imm[10:20]+imm[9]+imm[1:9]+res+"1101111")
    
def b_inst (type, arg1, arg2, imm, line_num):
    #imm[12|10:5]/rs2/rs1/funct3/imm[4:1|11]/opcode
    arg1 = reg_translator(arg1)
    arg2 = reg_translator(arg2)
    try:
        imm = to_bin(int(imm,0), 13)
    except ValueError:
        imm = (label_adress(imm) - line_num)*4
        imm = to_bin(imm, 13)
    if type == "beq":
        return to_hex(imm[0]+imm[2:8]+arg2+arg1+"000"+imm[8:12]+imm[1]+"1100011")
    elif type == "bne":
        return to_hex(imm[0]+imm[2:8]+arg2+arg1+"001"+imm[8:12]+imm[1]+"1100011")

def u_inst (type, res, imm):
    #imm[31:12]/rd/opcode
    res = reg_translator(res)
    imm = to_bin(int(imm,0), 20)
    if type == "lui":
        return to_hex(imm+res+"0110111")
    elif type == "auipc":
        return to_hex(imm+res+"0010111")

def splitter(inst):
    inst = inst.replace(",", " ")
    inst = inst.replace("(", " ")
    inst = inst.replace(")", " ")
    return inst.split()

def inst_parser(inst,line_num):
    inst = splitter(inst)

    r_type = ["add", "sub", "and", "or", "xor", "slt", "sll", "srl"]
    i_type = ["lw", "addi", "jalr", "slti", "andi", "ori", "xori", "lhu"]
    s_type = ["sw"]
    u_type = ["lui", "auipc"]
    j_type = ["jal"]
    b_type = ["beq", "bne"]

    if inst[0] in r_type:
        return r_inst(inst[0], inst[1], inst[2], inst[3])
    elif inst[0] in i_type:
        return i_inst(inst[0], inst[1], inst[2], inst[3])
    elif inst[0] in s_type:
        return s_inst(inst[0], inst[1], inst[2], inst[3])
    elif inst[0] in j_type:
        if len(inst) == 2:
            inst.insert(1, "ra")
        return j_inst(inst[0], inst[1], inst[2], line_num)
    elif inst[0] in b_type:
        return b_inst(inst[0], inst[1], inst[2], inst[3], line_num)
    elif inst[0] in u_type:
        return u_inst(inst[0], inst[1], inst[2])
    else:
        raise ValueError("Invalid instruction type: " + inst[0])

def memory_size(type):
    #Retorna o número de casas que um tipo de dado ocupa no código hexadecimal
    if type == ".word":
        return 8
    elif type == ".half":
        return 4
    elif type == ".byte" or type == ".string":
        return 2
    else:
        raise ValueError("Invalid memory reservation type: " + type)

def data_parser(data):
    #Recebe uma string com todas as linhas do bloco .data
    #Retorna uma lista de strings representando os dados em hexadecimal
    memory = []
    output = []
    data = data.splitlines()
    for line in data:
        line = splitter(line)
        if line[1] == ".string":
            line = string_handler(line)
        for i in range(2, len(line)):
            if len(memory) > 10-memory_size(line[1]):
                remainder = int("".join(memory), 16)
                output.append("".join((to_hex(to_bin(remainder, 32)))))
                memory = []
            if len(memory) == 0:
                memory = list(to_hex(to_bin(int(line[i],0), memory_size(line[1])*4), memory_size(line[1])))
            else:
                memory[2:2] = list(to_hex(to_bin(int(line[i],0), memory_size(line[1])*4), memory_size(line[1]))[2:])
    remainder = int("".join(memory), 16)
    output.append("".join((to_hex(to_bin(remainder, 32)))))
    return output

def string_handler(line):
    #Retorna a linha em forma de lista, mas com os caracteres transformados em ascii
    string = " ".join(line[2:])
    output = []
    output.append(line[0])
    output.append(line[1])
    for char in string:
        if char != '"' and char != "'":
            output.append(str(ord(char)))
    return output

def code_instructions(instructions):
    #Retorna uma lista de strings representando as instruções em hexadecimal
    output = []
    for line in instructions:
        output.append(inst_parser(line, instructions.index(line)+1))
    return output

def header_mif(memory_size):
    return f"""DEPTH = {memory_size};
WIDTH = 32;
ADDRESS_RADIX = HEX;
DATA_RADIX = HEX;
CONTENT
BEGIN
"""

def create_data_file(data, origin_file):
    data_file = origin_file[:-4] + "_data" +".mif"
    with open(data_file, "w") as file:
        memory_size = 32768
        file.write(header_mif(memory_size))
        for i in range(memory_size//32):
            if i < len(data):
                file.write(to_hex(to_bin(i, 32))[2:] + " : " + data[i][2:] + ";\n")
            else:
                file.write(to_hex(to_bin(i, 32))[2:] + " : 00000000;\n")
        file.write("END;")

def create_text_file(instructions, origin_file):
    inst_file = origin_file[:-4] + "_text" +".mif"
    with open(inst_file, "w") as file:
        memory_size = 16384
        file.write(header_mif(memory_size))
        for i in range(len(instructions)):
            file.write(to_hex(to_bin(i, 32))[2:] + " : " + instructions[i][2:] + ";\n")
        file.write("END;")

def map_labels(instructions):
    #Mapeia as labels
    without_label = []
    for line in instructions:
        if line.find(":") != -1:
            if line[:line.find(":")] != '':
                labels[line[:line.find(":")]] = instructions.index(line)+1
            try:
                #Verifica se o resto da linha é uma instrução
                remain = line[line.find(":")+1:]
                inst_parser(remain,instructions.index(line))
                without_label.append(remain)
            except:
                pass
        else:
            without_label.append(line)
    return without_label

def main():
    while True:
        file_name = input("Enter the name of the .asm file (0 to exit): ")
        if file_name == "0":
            exit()
        try:
            if not ".asm" in file_name:
                raise ValueError("Invalid file type: " + file_name)
            with open(file_name, "r") as file:
                lines = file.readlines()
                break
        except FileNotFoundError:
            print("File not found: " + file_name)
        except ValueError as e:
            print(str(e))
        except Exception as e:
            print("Error: " + str(e))

    data = ""
    instructions = []

    data_block = False
    for line in lines:
        if not line.strip() == '':
            if line.strip() == ".data":
                data_block = True
            elif line.strip() == ".text":
                data_block = False
            elif data_block:
                data += line.strip() + "\n"
            else:
                instructions.append(line.strip()) 

    instructions = map_labels(instructions)

    try:
        if data != "":
            coded_data = data_parser(data)
            create_data_file(coded_data, file_name)
    except Exception as e:
        print("Error with .data field: " + str(e))
    try:
        if instructions != []:
            coded_instructions = code_instructions(instructions)
            create_text_file(coded_instructions, file_name)
    except Exception as e:
        print("Error with .text field: " + str(e))

main()