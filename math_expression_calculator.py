import math
import operator as op
from pyparsing import (
    Word, alphas, nums, Literal, Forward, Group, Optional, oneOf, Combine, ZeroOrMore, ParseException
)

def parse_math(text):
    """
    주어진 텍스트에서 수식을 추출하는 함수.

    Args:
        text (str): 수식으로 변환할 문자열.

    Returns:
        list: 파싱된 수식의 요소들을 리스트 형태로 반환.
        str: 파싱 오류 발생 시 오류 메시지 반환.

    예외:
        ParseException: 파싱 과정에서 오류 발생 시 예외 처리.
    """
    try:
        # 기본 요소 정의
        # 숫자 정의: 부호, 정수부, 소수점, 소수부, 지수부를 포함할 수 있음
        number = Combine(Optional(oneOf("+ -")) + Word(nums) + 
                        Optional("." + Optional(Word(nums))) + 
                        Optional(oneOf("e E") + Optional(oneOf("+ -")) + Word(nums)))    
        # 변수 정의: 알파벳으로 시작하고, 숫자를 포함할 수 있음
        variable = Combine(Word(alphas) + Optional(Word(nums)))
        operand = number | variable
        
        # 연산자 정의
        exp_op = Literal('^')   # 지수 연산
        mult_op = oneOf('* /')  # 곱셈, 나눗셈
        add_op = oneOf('+ -')   # 덧셈, 뺄셈
        
        # 괄호 정의
        lpar = Literal('(').suppress()  # 왼쪽 괄호
        rpar = Literal(')').suppress()  # 오른쪽 괄호
        
        # 전방 참조를 위한 표현식
        expr = Forward()
        
        # 수학 함수 정의
        math_function = oneOf('log10 ln sin cos tan exp sqrt abs')
        math_func_expr = Group(math_function + lpar + Group(expr) + rpar)

        # 단일 요소, 괄호, 함수 표현식 정의
        atom = math_func_expr | operand | Group(lpar + expr + rpar)
        factor = Forward()
        factor <<= atom + ZeroOrMore((exp_op + atom))
        term = factor + ZeroOrMore((mult_op + factor))
        expr <<= term + ZeroOrMore((add_op + term))
        
        # 최종 수식 정의 및 파싱 실행
        math_expr = expr
        parsed_expressions = math_expr.parseString(text, parseAll=True).asList()

        return parsed_expressions
    except ParseException:
        return "Error: Invalid Syntax"

class MathExpressionCalculator:
    """
    수학 표현식을 계산하는 클래스.

    Attributes:
        operators (dict): 기본 연산자와 해당 연산을 수행하는 함수의 매핑.
        functions (dict): 수학 함수 이름과 해당 함수의 매핑.

    Methods:
        perform_operation: 주어진 연산자와 피연산자를 사용하여 연산 수행.
        calculate_expression: 표현식을 계산.
        calculate_formula: 수식 문자열과 변수를 받아 계산 결과 반환.
    
    Examples:
        # 예시 사용
        calculator = MathExpressionCalculator()
        variables0 = {'a': 1.0, 'X1': 3.0, 'b': 2.0, 'X2': 4.0}
        print(calculator.calculate_formula('a * X1 + b / X2', a=1.0, X1=3.0, b=2.0, X2=4.0))
        print(calculator.calculate_formula('a * X1 + b / X2', variables_dict={'a': 1.0, 'X1': 3.0, 'b': 2.0, 'X2': 4.0}))
        print(calculator.calculate_formula('a * X1 + b / X2', **variables0))    
    """
    operators = {
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv, '^': op.pow
    }
    functions = {
        'log10': math.log10, 'ln': math.log, 'exp': math.exp, 
        'sqrt': math.sqrt, 'abs': math.fabs,
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 
    }

    @staticmethod
    def perform_operation(left, operator, right):
        """
        주어진 연산자와 피연산자를 사용하여 연산 수행.

        Args:
            left (float): 왼쪽 피연산자.
            operator (str): 연산자.
            right (float): 오른쪽 피연산자.

        Returns:
            float: 연산 결과.
        """
        # 숫자 또는 변수일 경우
        if operator == '^' and isinstance(right, str) and right.startswith('-'):
            right = float(right[1:])
            return 1 / MathExpressionCalculator.operators[operator](left, right)
        else:
            return MathExpressionCalculator.operators[operator](left, right)

    @staticmethod
    def calculate_expression(expression, variables):
        """
        주어진 표현식을 계산.

        Args:
            expression: 계산할 표현식.
            variables (dict): 변수명과 값을 매핑하는 사전.

        Returns:
            float: 계산 결과.
        """
        if isinstance(expression, str):
            if expression.lstrip('-').replace('.', '', 1).isdigit() or 'e' in expression:
                return float(expression)
            else:
                if expression in variables:
                    return variables.get(expression)
                else:
                    raise ValueError("Variable not found.")

        if isinstance(expression, (int, float)):
            return expression

        # 표현식 처리
        if len(expression) == 1:
            return MathExpressionCalculator.calculate_expression(expression[0], variables)

        elif len(expression) == 3:
            left, operator, right = expression
            left_val = MathExpressionCalculator.calculate_expression(left, variables)
            right_val = MathExpressionCalculator.calculate_expression(right, variables)
            # 두 피연산자 모두 숫자형인지 확인
            if not isinstance(left_val, (int, float)) or not isinstance(right_val, (int, float)):
                return f"Error: unsupported operand type(s) for {operator}: '{type(left_val).__name__}' and '{type(right_val).__name__}'"

            return MathExpressionCalculator.perform_operation(left_val, operator, right_val)

        if isinstance(expression[0], str) and expression[0] in MathExpressionCalculator.functions:
            func = MathExpressionCalculator.functions[expression[0]]
            arg = MathExpressionCalculator.calculate_expression(expression[1], variables)
            return func(arg)

        # 연산자 우선순위에 따른 계산 로직
        while '^' in expression:
            for i, op in enumerate(expression):
                if op == '^':
                    left = MathExpressionCalculator.calculate_expression(expression[i - 1], variables)
                    right = MathExpressionCalculator.calculate_expression(expression[i + 1], variables)
                    result = MathExpressionCalculator.operators[op](left, right)
                    expression[i - 1:i + 2] = [result]
                    break

        while '*' in expression or '/' in expression:
            for i, op in enumerate(expression):
                if op in ['*', '/']:
                    left = MathExpressionCalculator.calculate_expression(expression[i - 1], variables)
                    right = MathExpressionCalculator.calculate_expression(expression[i + 1], variables)
                    result = MathExpressionCalculator.operators[op](left, right)
                    expression[i - 1:i + 2] = [result]
                    break

        result = MathExpressionCalculator.calculate_expression(expression[0], variables)
        for i in range(1, len(expression), 2):
            operator = expression[i]
            next_expr = expression[i + 1]
            next_value = MathExpressionCalculator.calculate_expression(next_expr, variables)
            result = MathExpressionCalculator.operators[operator](result, next_value)

        return result

    @staticmethod
    def calculate_formula(formula, variables_dict=None, **variables):
        """
        주어진 수식 문자열과 변수를 받아 계산 결과를 반환.

        Args:
            formula (str): 계산할 수식 문자열.
            variables_dict (dict, optional): 변수명과 값을 매핑하는 사전.
            **variables: 추가적인 변수 매핑.

        Returns:
            float: 계산 결과.
        """
        if variables_dict:
            variables.update(variables_dict)

        try:
            expressions = parse_math(formula)
            if isinstance(expressions, str) and expressions.startswith("Error:"):
                return expressions
            return MathExpressionCalculator.calculate_expression(expressions, variables)
        
        except ValueError as e:
            return f"Error: {str(e)}"
        
        except Exception as e:
            return f"Error: {str(e)}"