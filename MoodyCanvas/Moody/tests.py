from django.test import TestCase
import unittest
from django.test import Client
from Moody.models import Customer, Plate, Verif, Profile, Meas
from Moody.utils import sub_first, add_rows, process_diag, process_line, get_mid, get_height_map, get_min, get_max, get_flatness, grade, get_grade, get_closure
from Moody.views import save_new_verif

class SubFirstTest(TestCase):
    def setUp(self):
        self.line12 = [12.3, 11.40, ]
        self.line18 = [0, 1, 2, 3, ]
        self.line24 = [-5, 10, -15, 20, -15, 25, ]
        self.line36 = [7.80, 7.97, 7.50, 6.70, 6.77, 7.20, 6.50, 5.37, ]
        self.line48 = [4.43, 4.53, 3.83, 3.00, 3.67, 4.60, 4.50, 5.30, 4.93, 5.17, ]
        self.line72 = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 140, 160, 180, 200, 220, ]
        self.line144 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, ]

    def test_line12(self):  #   Minimum number of measurements
        self.assertEqual(sub_first(self.line12), [0, -0.90, ])
    
    def test_line18(self):  #   Output should match input
        self.assertEqual(sub_first(self.line18), [0, 1, 2, 3, ])

    def test_line24(self):  #   Negative first element
        self.assertEqual(sub_first(self.line24), [0, 15, -10, 25, -10, 30, ])

    def test_line36(self):
        self.assertEqual(sub_first(self.line36), [0, 0.17, -0.30, -1.10, -1.03, -0.60, -1.30, -2.43, ])

    def test_line48(self):
        self.assertEqual(sub_first(self.line48), [0, 0.1, -0.60, -1.43, -0.76, 0.17, 0.07, 0.87, 0.50, 0.74, ])

    def test_line72(self):
        self.assertEqual(sub_first(self.line72), [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, ])

    def test_line144(self):
        self.assertEqual(sub_first(self.line144), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, ])


class AddRowsTest(TestCase):
    def setUp(self):
        self.line12 = [0, -0.90, ]
        self.line18 = [0, 1, 2, 3, ]
        self.line24 = [0, 15, -10, 25, -10, 30 ]
        self.line36 = [0, 0.17, -0.30, -1.10, -1.03, -0.60, -1.30, -2.40,  ]
        self.line48 = [0, 0.10, -0.60, -1.43, -0.76, 0.17, 0.07, 0.87, 0.50, 0.74, ]
        self.line72 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, ]
        self.line144 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, ]

    def test_line12(self):  #   Minimum number of measurements
        self.assertEqual(add_rows(self.line12), [0, 0, -0.90, ])
    
    def test_line18(self):  #   Output should match input
        self.assertEqual(add_rows(self.line18), [0, 0, 1, 3, 6, ])

    def test_line24(self):  #   Negative first element
        self.assertEqual(add_rows(self.line24), [0, 0, 15, 5, 30, 20, 50, ])

    def test_line36(self):
        self.assertEqual(add_rows(self.line36), [0, 0, 0.17, -0.13, -1.23, -2.26, -2.86, -4.16, -6.56, ])

    def test_line48(self):
        self.assertEqual(add_rows(self.line48), [0, 0, 0.1, -0.50, -1.93, -2.69, -2.52, -2.45, -1.58, -1.08, -0.34, ])

    def test_line72(self):
        self.assertEqual(add_rows(self.line72), [0, 0, 10, 30, 60, 100, 150, 210, 280, 360, 450, 550, 670, 810, 970, 1150, 1350, ])

    def test_line144(self):
        self.assertEqual(add_rows(self.line144), [0, 0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136, 153, 171, 190, 210, 231, 253, 276, 300, 325, 351, 378, 406, 435, 465, 496, 528, 561, 595, 630, 666, 703, ])
