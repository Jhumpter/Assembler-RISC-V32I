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
    if type == "add":
        return "0000000"+arg2+arg1+"000"+res+"0110011"
    elif type == "sub":
        return "0100000"+arg2+arg1+"000"+res+"0110011"
    elif type == "and":
        return "0000000"+arg2+arg1+"111"+res+"0110011"
    elif type == "or":
        return "0000000"+arg2+arg1+"110"+res+"0110011"
    elif type == "xor":
        return "0000000"+arg2+arg1+"100"+res+"0110011"
    elif type == "slt":
        return "0000000"+arg2+arg1+"010"+res+"0110011"
    elif type == "sll":
        return "0000000"+arg2+arg1+"001"+res+"0110011"
    elif type == "srl":
        return "0000000"+arg2+arg1+"101"+res+"0110011"

def i_inst (type, res, arg1, imm):
    #imm[11:0]/rs1/funct3/rd/opcode
    imm = to_bin(int(imm), 12)
    if type == "lw":
        return imm+arg1+"010"+res+"0000011"
    elif type == "addi":
        return imm+arg1+"000"+res+"0010011"
    elif type == "jalr":
        return imm+arg1+"000"+res+"1100111"
    elif type == "slti":
        return imm+arg1+"010"+res+"0010011"
    elif type == "andi":
        return imm+arg1+"111"+res+"0010011"
    elif type == "ori":
        return imm+arg1+"110"+res+"0010011"
    elif type == "xori":
        return imm+arg1+"100"+res+"0010011"
    elif type == "lhu":
        return imm+arg1+"101"+res+"0000011"

def s_inst (type, arg1, arg2, imm):
    #imm[11:5]/rs2/rs1/funct3/imm[4:0]/opcode
    imm = to_bin(int(imm), 12)
    if type == "sw":
        return imm[:8]+arg2+arg1+"010"+imm[7:]+"0100011"

def u_inst (type, res, imm):
    #imm[31:12]/rd/opcode

    imm = to_bin(int(imm), 20)
    if type == "lui":
        return imm+res+"0110111"
    elif type == "auipc":
        return imm+res+"0010111"

def j_inst (type, res, imm):
    #imm[20|10:1|11|19:12]/rd/opcode
    #Na instrução tipo J vai ser necessário encontrar o endereço de "Label:" e calcular o valor de imm a partir disso

    imm = to_bin(int(imm), 21)
    if type == "jal":
        return imm[0]+imm[10:20]+imm[9]+imm[1:9]+res+"1101111"
    
def b_inst (type, arg1, arg2, imm):
    #imm[12|10:5]/rs2/rs1/funct3/imm[4:1|11]/opcode

    imm = to_bin(int(imm), 13)
    if type == "beq":
        return imm[0]+imm[2:8]+arg2+arg1+"000"+imm[8:12]+imm[1]+"1100011"
    elif type == "bne":
        return imm[0]+imm[2:8]+arg2+arg1+"001"+imm[8:12]+imm[1]+"1100011"

#Será necessário avaliar a base do número fornecido

#Testing

#R-type
inst = "add t0, s0, s1"
inst = inst.replace(",", " ")
inst = inst.split()
inst = r_inst(inst[0], reg_translator(inst[1]), reg_translator(inst[2]), reg_translator(inst[3]))
inst = hex(int(inst, 2))
print(inst)

#I-type
inst = "addi t0,s0,255"
inst = inst.replace(",", " ")
inst = inst.split()
inst = i_inst(inst[0], reg_translator(inst[1]), reg_translator(inst[2]), inst[3])
inst = hex(int(inst, 2))
print(inst)

#S-type
inst = "sw s0,4(s1)"
inst = inst.replace(",", " ")
inst = inst.replace("(", " ")
inst = inst.replace(")", " ")
inst = inst.split()
inst = s_inst(inst[0], reg_translator(inst[3]), reg_translator(inst[1]), inst[2])
inst = hex(int(inst, 2))
print(inst)

#J-type
#Supondo que o endereço de "Label:" seja 2 linhas atrás de PC
inst = "jal ra, -8"
inst = inst.replace(",", " ")
inst = inst.split()
inst = j_inst(inst[0], reg_translator(inst[1]), inst[2])
inst = hex(int(inst, 2))
print(inst)

#B-type
#Supondo que o endereço de "Label:" seja 3 linhas atrás de PC
inst = "beq t0,t1,-12"
inst = inst.replace(",", " ")
inst = inst.split()
inst = b_inst(inst[0], reg_translator(inst[1]), reg_translator(inst[2]), inst[3])
inst = hex(int(inst, 2))
print(inst)


#U-type
inst = "lui t0, 74565"
inst = inst.replace(",", " ")
inst = inst.split()
inst = u_inst(inst[0], reg_translator(inst[1]), inst[2])
inst = hex(int(inst, 2))
print(inst)

