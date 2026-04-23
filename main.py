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
    