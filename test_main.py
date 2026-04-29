import unittest
from main import *

class TestMain(unittest.TestCase):
    def test_r_inst(self):
        inst = "add t0, s0, s1"
        inst = inst.replace(",", " ")
        inst = inst.split()
        inst = r_inst(inst[0], reg_translator(inst[1]), reg_translator(inst[2]), reg_translator(inst[3]))
        inst = to_hex(inst)
        self.assertEqual(inst, "0x009402b3")

    def test_i_inst(self):
        inst = "addi t0,s0,255"
        inst = inst.replace(",", " ")
        inst = inst.split()
        inst = i_inst(inst[0], reg_translator(inst[1]), reg_translator(inst[2]), inst[3])
        inst = to_hex(inst)
        self.assertEqual(inst, "0x0ff40293")

    def test_s_inst(self):
        inst = "sw s0,4(s1)"
        inst = inst.replace(",", " ")
        inst = inst.replace("(", " ")
        inst = inst.replace(")", " ")
        inst = inst.split()
        inst = s_inst(inst[0], reg_translator(inst[3]), reg_translator(inst[1]), inst[2])
        inst = to_hex(inst)
        self.assertEqual(inst, "0x0084a223")

    def test_j_inst(self):
        #Supondo que o endereço de "Label:" seja 2 linhas atrás de PC
        inst = "jal ra, -8"
        inst = inst.replace(",", " ")
        inst = inst.split()
        inst = j_inst(inst[0], reg_translator(inst[1]), inst[2])
        inst = to_hex(inst)
        self.assertEqual(inst, "0xff9ff0ef")

    def test_b_inst(self):
        #Supondo que o endereço de "Label:" seja 3 linhas atrás de PC
        inst = "beq t0,t1,-12"
        inst = inst.replace(",", " ")
        inst = inst.split()
        inst = b_inst(inst[0], reg_translator(inst[1]), reg_translator(inst[2]), inst[3])
        inst = to_hex(inst )
        self.assertEqual(inst, "0xfe628ae3")

    def test_u_inst(self):
        inst = "lui t0, 74565"
        inst = inst.replace(",", " ")
        inst = inst.split()
        inst = u_inst(inst[0], reg_translator(inst[1]), inst[2])
        inst = to_hex(inst)
        self.assertEqual(inst, "0x123452b7")

if __name__ == '__main__':
    unittest.main()