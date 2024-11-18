import unittest

from task1.solution import sum_two


class TestAddFunction(unittest.TestCase):
    def test_sum_two(self):
        self.assertEqual(sum_two(2, 3), 5) 
        self.assertEqual(sum_two(-1, b=1), 0)   
        self.assertEqual(sum_two(a=0, b=0), 0)

        self.assertEqual(sum_two(False, True), 1) # bool is a subtype of int
        
        with self.assertRaises(TypeError):
            sum_two("1", "2")
            sum_two("1", 0)
            sum_two(0, "2")
            
            sum_two(True, b=0)
            sum_two(0, b=False)   

            self.assertEqual(sum_two(1.0, 1.2), 2.2)
