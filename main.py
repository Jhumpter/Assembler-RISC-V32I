def reg_translator(reg):
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

def to_hex(inst):
    #Passa o número binário para hexadecimal com 8 dígitos
    return "0x"+hex(int(inst, 2))[2:].zfill(8)

def to_bin(num, bits):
    #Calcula o complemento de 2 para números negativos e retorna a representação binária de num com o número de bits especificado
    if num >=0:
        return bin(num)[2:].zfill(bits)
    elif num < 0:
        return bin((1 << bits) + num)[2:]
    else:
        raise ValueError("Invalid number: " + str(num))

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

def j_inst (type, res, imm):
    #imm[20|10:1|11|19:12]/rd/opcode
    res = reg_translator(res)
    imm = to_bin(int(imm,0), 21)
    if type == "jal":
        return to_hex(imm[0]+imm[10:20]+imm[9]+imm[1:9]+res+"1101111")
    
def b_inst (type, arg1, arg2, imm):
    #imm[12|10:5]/rs2/rs1/funct3/imm[4:1|11]/opcode
    arg1 = reg_translator(arg1)
    arg2 = reg_translator(arg2)
    imm = to_bin(int(imm,0), 13)
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

def inst_splitter(inst):
    inst = inst.replace(",", " ")
    inst = inst.replace("(", " ")
    inst = inst.replace(")", " ")
    return inst.split()

def inst_parser(inst):
    inst = inst_splitter(inst)

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
        return j_inst(inst[0], inst[1], inst[2])
    elif inst[0] in b_type:
        return b_inst(inst[0], inst[1], inst[2], inst[3])
    elif inst[0] in u_type:
        return u_inst(inst[0], inst[1], inst[2])
    else:
        raise ValueError("Invalid instruction type: " + inst[0])

'''
entry = input("Enter a instruction (0 to exit): ")
while entry != "0":
    try:
        print(inst_parser(entry))
    except ValueError as e:
        print(e)
    entry = input("Enter a instruction (0 to exit): ")
'''

#To-do:

#Implementar a leitura de um arquivo .asm e a escrita de um arquivo .mif
#Vai ser necessário encontrar o endereço de "Label:" e calcular o valor de imm a partir disso
#Fazer interface
#Separação entre os campos .text e .data
#Se jal não tiver um registrador, usar ra por padrão