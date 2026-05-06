import unittest
from main import *

class TestMain(unittest.TestCase):
    def test_r_inst(self):
        inst = "add t0, s0, s1"
        inst = inst_parser(inst,1)
        self.assertEqual(inst, "0x009402b3")

    def test_i_inst(self):
        inst = "addi t0,s0,255"
        inst = inst_parser(inst,1)
        self.assertEqual(inst, "0x0ff40293")

    def test_s_inst(self):
        inst = "sw s0,4(s1)"
        inst = inst_parser(inst,1)
        self.assertEqual(inst, "0x0084a223")

    def test_j_inst(self):
        #Supondo que o endereço de "Label:" seja 2 linhas atrás de PC (L*4)
        inst = "jal ra, -8"
        inst = inst_parser(inst,1)
        self.assertEqual(inst, "0xff9ff0ef")

    def test_j_inst(self):
        #Supondo que o endereço de "Label:" seja 3 linhas a frente de PC (L*4)
        inst = "jal, 12"
        inst = inst_parser(inst,1)
        self.assertEqual(inst, "0x00c000ef")

    def test_b_inst(self):
        #Supondo que o endereço de "Label:" seja 3 linhas atrás de PC (L*4)
        inst = "beq t0,t1,-12"
        inst = inst_parser(inst,1)
        self.assertEqual(inst, "0xfe628ae3")

    def test_u_inst(self):
        inst = "lui t0, 74565"
        inst = inst_parser(inst,1)
        self.assertEqual(inst, "0x123452b7")

    def test1(self):
        inst = "lw t2, 0(t1)"
        inst = inst_parser(inst,1)
        self.assertEqual(inst, "0x00032383")

    def test2(self):
        inst = "sw t2, 32(t1)"
        inst = inst_parser(inst,1)
        self.assertEqual(inst, "0x02732023")

    def test3(self):
        inst = "lhu t5, 32(t1)"
        inst = inst_parser(inst,1)
        self.assertEqual(inst, "0x02035f03")

    def test_data_parser(self):
        data = """dado_byte:  .byte 0x10, 0x20
dado_word:  .word 0xAABBCCDD   
dado_half:  .half 0x1122
dado_byte2: .byte 0xEE"""
        result = ['0x00002010', '0xaabbccdd', '0x00ee1122']
        self.assertEqual(data_parser(data), result)

    def test_data_parser2(self):
        data = """val1: .word 0x12345678
val2: .half 0xABCD
val3: .byte 0xFF"""
        result = ['0x12345678', '0x00ffabcd']
        self.assertEqual(data_parser(data), result)

    def test_data_parser3(self):
        data = """a: .word 1, 2, 3, 4, 5
b: .half 7, 6, 5, 4, 5
c: .byte 6, 5, 4, 3, 2"""
        result = ['0x00000001', '0x00000002', '0x00000003', '0x00000004', '0x00000005', '0x00060007', '0x00040005', '0x05060005', '0x00020304']
        self.assertEqual(data_parser(data), result)

    def test_data_parser4(self):
        data = """max_uint:   .word 0xFFFFFFFF
max_int:    .word 2147483647
min_int:    .word -2147483648
zero:       .word 0"""
        result = ['0xffffffff', '0x7fffffff', '0x80000000', '0x00000000']
        self.assertEqual(data_parser(data), result)

if __name__ == '__main__':
    unittest.main()