def Rinst (type, res, arg1, arg2):
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

def Iinst (type, res, arg1, imm):
    #imm[11:0]/rs1/funct3/rd/opcode
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

def Sinst (type, arg1, arg2, imm):
    #imm[11:5]/rs2/rs1/funct3/imm[4:0]/opcode
    if type == "sw":
        return imm[11:5]+arg2+arg1+"010"+imm+"0100011"
    
def Uinst (type, res, imm):
    #imm[31:12]/rd/opcode
    if type == "lui":
        return imm+res+"0110111"
    elif type == "auipc":
        return imm+res+"0010111"
