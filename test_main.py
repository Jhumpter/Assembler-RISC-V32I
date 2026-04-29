import unittest
from main import *

class TestMain(unittest.TestCase):
    def test_r_inst(self):
        inst = "add t0, s0, s1"
        inst = inst_parser(inst)
        self.assertEqual(inst, "0x009402b3")

    def test_i_inst(self):
        inst = "addi t0,s0,255"
        inst = inst_parser(inst)
        self.assertEqual(inst, "0x0ff40293")

    def test_s_inst(self):
        inst = "sw s0,4(s1)"
        inst = inst_parser(inst)
        self.assertEqual(inst, "0x0084a223")

    def test_j_inst(self):
        #Supondo que o endereço de "Label:" seja 2 linhas atrás de PC (L*4)
        inst = "jal ra, -8"
        inst = inst_parser(inst)
        self.assertEqual(inst, "0xff9ff0ef")

    def test_j_inst(self):
        #Supondo que o endereço de "Label:" seja 3 linhas a frente de PC (L*4)
        inst = "jal, 12"
        inst = inst_parser(inst)
        self.assertEqual(inst, "0x00c000ef")

    def test_b_inst(self):
        #Supondo que o endereço de "Label:" seja 3 linhas atrás de PC (L*4)
        inst = "beq t0,t1,-12"
        inst = inst_parser(inst)
        self.assertEqual(inst, "0xfe628ae3")

    def test_u_inst(self):
        inst = "lui t0, 74565"
        inst = inst_parser(inst)
        self.assertEqual(inst, "0x123452b7")

    def test1(self):
        inst = "lw t2, 0(t1)"
        inst = inst_parser(inst)
        self.assertEqual(inst, "0x00032383")

    def test2(self):
        inst = "sw t2, 32(t1)"
        inst = inst_parser(inst)
        self.assertEqual(inst, "0x02732023")

    def test3(self):
        inst = "lhu t5, 32(t1)"
        inst = inst_parser(inst)
        self.assertEqual(inst, "0x02035f03")

if __name__ == '__main__':
    unittest.main()