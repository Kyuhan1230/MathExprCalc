import unittest
import math
from math_expression_calculator import MathExpressionCalculator

class TestMathExpressionCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = MathExpressionCalculator()

    def test_basic_arithmetic(self):
        result = self.calculator.calculate_formula("3 + 4 * 2 - 1", {})
        self.assertEqual(result, 10)

    def test_with_variables(self):
        variables = {'x': 4, 'y': 2}
        result = self.calculator.calculate_formula("x * y + 3", variables)
        self.assertEqual(result, 11)

    def test_advanced_functions(self):
        result = self.calculator.calculate_formula("sin(0) + cos(0)", {})
        self.assertAlmostEqual(result, 1, places=5)

    def test_custom_test_cases(self):
        test_cases = [
            # 1. 다양한 수학 연산 케이스
            ("a + b", {'a': 1, 'b': 2}, 3),
            ("a - b", {'a': 5, 'b': 2}, 3),
            ("a * b", {'a': 3, 'b': 4}, 12),
            ("a / b", {'a': 8, 'b': 2}, 4),
            ("a * (b + c)", {'a': 2, 'b': 3, 'c': 4}, 14),
            ("(a + b) / (c - d)", {'a': 5, 'b': 3, 'c': 10, 'd': 2}, 1),
            ("a ^ b", {'a': 2, 'b': 3}, 8),
            ("a * b + c / d", {'a': 2, 'b': 3, 'c': 4, 'd': 2}, 8),
            ("a * (b + c) / d", {'a': 2, 'b': 3, 'c': 1, 'd': 2}, 4),
            ("(a + b) ^ (c - d)", {'a': 1, 'b': 1, 'c': 3, 'd': 1}, 4),

            # 2. 변수와 상수의 조합 케이스
            ("3 * X1 + 4 * X2 - X3", {'X1': 1, 'X2': 1, 'X3': 1}, 6),
            ("X1 * X2 / X3 + X4 - 5", {'X1': 2, 'X2': 2, 'X3': 2, 'X4': 5}, 2),
            ("X1 + X2 * X3 - X4 / 2 + X5", {'X1': 1, 'X2': 2, 'X3': 3, 'X4': 4, 'X5': 5}, 10),
            ("(X1 + 3) * (X2 - X3) / X4", {'X1': 1, 'X2': 5, 'X3': 2, 'X4': 2}, 6),
            ("2 * X1 + 3 * X2 - 4 / X3 + X4 * X5 - X6", {'X1': 1, 'X2': 1, 'X3': 2, 'X4': 1, 'X5': 1, 'X6': 1}, 3),
            ("X1 ^ X2 + X3 / X4 - X5 * 2", {'X1': 2, 'X2': 2, 'X3': 4, 'X4': 2, 'X5': 1}, 4),
            ("(X1 + X2) * (X3 - X4) / (X5 + X6)", {'X1': 1, 'X2': 2, 'X3': 5, 'X4': 3, 'X5': 2, 'X6': 1}, 2),
            ("(X1 + 2) * X2 / (X3 - 3) + X4 - X5", {'X1': 1, 'X2': 2, 'X3': 5, 'X4': 1, 'X5': 1}, 3),
            ("3 * X1 + (X2 - 5) * (X3 + X4) / X5", {'X1': 1, 'X2': 6, 'X3': 2, 'X4': 1, 'X5': 2}, 4.5),
            ("X1 * X2 - (X3 + 4) * (X4 - X5) + X6 / X7", {'X1': 1, 'X2': 2, 'X3': 3, 'X4': 4, 'X5': 2, 'X6': 8, 'X7': 4}, -10),
            
            # 3. 다양한 수학 함수 케이스
            ("log10(a * b) + c", {'a': 10, 'b': 1, 'c': 2}, math.log10(10)+2),  # log(10) = 1
            ("sin(a) * cos(b) - tan(c)", {'a': 0, 'b': 0, 'c': 0}, 0),  # sin(0) = 0, cos(0) = 1, tan(0) = 0
            ("exp(a + b) - c", {'a': 1, 'b': 1, 'c': 7.4}, math.exp(2)-7.4),  # exp(2) - exp(2) = 0
            ("sqrt(a^2 + b^2)", {'a': 3, 'b': 4}, 5),  # sqrt(9 + 16) = 5
            ("abs(a - b) + c", {'a': 5, 'b': 10, 'c': 3}, 8),  # abs(-5) + 3 = 8
            ("ln(a) + b", {'a': math.e, 'b': 2}, 3),  # ln(e) = 1
            ("ln(a * b) - c", {'a': math.e, 'b': math.e, 'c': 2}, 0),  # ln(e^2) - 2 = 0

            # 4. 경계값 테스트 케이스
            ("1e10 + X1", {'X1': 1}, 10000000001),
            ("X1 - 1e-10", {'X1': 1}, 0.9999999999),
            ("X1 / 1e10", {'X1': 1}, 1e-10),
            ("1e-10 * X1", {'X1': 1}, 1e-10),
            ("X1 ^ 100", {'X1': 2}, 2**100),
            ("1e10 ^ X1", {'X1': 1}, 1e10),
            ("X1 ^ -10", {'X1': 2}, 2**-10),
            ("X1 + (-1e10)", {'X1': 1}, -9999999999),
            ("(-1e-10) * X1", {'X1': 1}, -1e-10),
            ("X1 / (-1e-10)", {'X1': 1}, -1e10),

            # 5. 예외 상황 케이스
            ("X1 / X2 + X3 / 0", {'X1': 1, 'X2': 1, 'X3': 1}, "Error: float division by zero"),
            ("X1 + X2 -", {'X1': 1, 'X2': 1}, "Error: Invalid Syntax"),
            ("* X1 + X2 - X3", {'X1': 1, 'X2': 1, 'X3': 1}, "Error: Invalid Syntax"),
            ("X1 ^ X2 + X3 ^", {'X1': 1, 'X2': 2, 'X3': 3}, "Error: Invalid Syntax"),
            ("X1 ++ X2 - X3", {'X1': 1, 'X2': 1, 'X3': 1}, "Error: Invalid Syntax"),
            ("(X1 + X2 - X3", {'X1': 1, 'X2': 1, 'X3': 1}, "Error: Invalid Syntax"),
            ("X1 + X2) - X3 + X4", {'X1': 1, 'X2': 1, 'X3': 1, 'X4': 1}, "Error: Invalid Syntax"),
            ("X1 + X5 - X2 + X6", {'X1': 1, 'X2': 1, 'X6': 1}, "Error: Variable not found."),
            ("X1 ^^ X2 - X3 + X4", {'X1': 1, 'X2': 1, 'X3': 1, 'X4': 1}, "Error: Invalid Syntax"),
            ("X1 + X2 / - X3 * X4", {'X1': 1, 'X2': 1, 'X3': 1, 'X4': 1}, "Error: Invalid Syntax"),
        ]
        for formula, variables, expected in test_cases:
            with self.subTest(formula=formula, variables=variables, expected=expected):
                result = self.calculator.calculate_formula(formula, variables_dict=variables)
                if isinstance(expected, list):
                    expected = expected[0]  # 리스트의 첫 번째 요소가 기대값
                self.assertEqual(result, expected)

    def test_invalid_syntax(self):
        result = self.calculator.calculate_formula("2 ** 3", {})
        self.assertEqual(result, "Error: Invalid Syntax")

if __name__ == '__main__':
    unittest.main()
