def reg_translator(reg):
    translator = ["00000","00001","00010","00011","00100","00101","00110","00111",
     "01000","01001","01010","01011","01100","01101","01110","01111",
     "10000","10001","10010","10011","10100","10101","10110","10111",
     "11000","11001","11010","11011","11100","11101","11110","11111"]
    if reg[0] == "x" and reg[1:].isdigit() and int(reg[1:]) >= 0 and int(reg[1:]) <= 31:
        return translator[int(reg[1:])]
    else:
        if reg == "zero":
            return translator[0]
        elif reg == "ra":
            return translator[1]
        elif reg == "sp":
            return translator[2]
        elif reg == "gp":
            return translator[3]
        elif reg == "tp":
            return translator[4]
        elif reg == "t0":
            return translator[5]
        elif reg == "t1":
            return translator[6]
        elif reg == "t2":
            return translator[7]
        elif reg == "s0" or reg == "fp":
            return translator[8]
        elif reg == "s1":
            return translator[9]
        elif reg == "a0":
            return translator[10]
        elif reg == "a1":
            return translator[11]
        elif reg == "a2":
            return translator[12]
        elif reg == "a3":
            return translator[13]
        elif reg == "a4":
            return translator[14]
        elif reg == "a5":
            return translator[15]
        elif reg == "a6":
            return translator[16]
        elif reg == "a7":
            return translator[17]
        elif reg == "s2":
            return translator[18]
        elif reg == "s3":
            return translator[19]
        elif reg == "s4":
            return translator[20]
        elif reg == "s5":
            return translator[21]
        elif reg == "s6":
            return translator[22]
        elif reg == "s7":
            return translator[23]
        elif reg == "s8":
            return translator[24]
        elif reg == "s9":
            return translator[25]
        elif reg == "s10":
            return translator[26]
        elif reg == "s11":
            return translator[27]
        elif reg =="t3":
            return translator[28]
        elif reg =="t4":
            return translator[29]
        elif reg =="t5":
            return translator[30]
        elif reg =="t6":
            return translator[31]
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
    if type == "sw":
        return imm[11:5]+arg2+arg1+"010"+imm+"0100011"
    
def u_inst (type, res, imm):
    #imm[31:12]/rd/opcode
    if type == "lui":
        return imm+res+"0110111"
    elif type == "auipc":
        return imm+res+"0010111"

def j_inst (type, res, imm):
    #imm[20|10:1|11|19:12]/rd/opcode
    if type == "jal":
        return imm+res+"1101111"
    
def b_inst (type, arg1, arg2, imm):
    #imm[12|10:5]/rs2/rs1/funct3/imm[4:1|11]/opcode
    if type == "beq":
        return imm[12]+imm[10:5]+arg2+arg1+"000"+imm[4:1]+imm[11]+"1100011"
    elif type == "bne":
        return imm[12]+imm[10:5]+arg2+arg1+"001"+imm[4:1]+imm[11]+"1100011"


#Testing

inst = "addi t0,s0,255"
inst = inst.replace(",", " ")
inst = inst.split()
inst = i_inst(inst[0], reg_translator(inst[1]), reg_translator(inst[2]), inst[3])
inst = hex(int(inst, 2))
print(inst)


