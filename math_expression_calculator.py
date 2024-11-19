# 작성자: 석규한
# 이메일: asdm159@naver.com

import numpy as np
# import math
# import operator as op
from pyparsing import (
    Word, alphas, nums, Forward, Group, Optional, oneOf, Combine, ParseException,
    infixNotation, opAssoc, Suppress, alphanums
)

def parse_math(expression):
    """
    수식을 파싱하여 중첩 리스트 형태로 반환합니다.

    Args:
        expression (str): 파싱할 수식 문자열.

    Returns:
        list or str: 파싱된 수식을 중첩 리스트 형태로 반환하거나, 파싱 오류 시 오류 메시지를 반환합니다.
    """
    try:
        # 숫자 파싱: 부호, 소수점, 지수 표기법을 지원
        number = Combine(
            Optional(oneOf("+ -")) + 
            Word(nums) +
            Optional("." + Word(nums)) +
            Optional(oneOf("e E") + Optional(oneOf("+ -")) + Word(nums))
        )
        
        # 변수 파싱: 알파벳이나 밑줄로 시작하고, 이후에는 알파벳, 숫자, 밑줄을 포함
        variable = Word(alphas + '_', alphanums + '_')
        
        # 피연산자는 숫자나 변수
        operand = number | variable

        # 함수 이름 파싱: 알파벳이나 밑줄로 시작하고, 이후에는 알파벳, 숫자, 밑줄을 포함
        function_name = Word(alphas + '_', alphanums + '_')
        expr = Forward()
        
        # 함수 호출 파싱: 함수 이름과 괄호 안의 표현식
        func = Group(function_name + Suppress('(') + expr + Suppress(')'))
        
        # 피연산자는 함수 또는 숫자/변수
        operand = func | operand

        # 연산자 우선순위 정의 (단항 연산자, 지수, 곱/나눗셈, 덧셈/뺄셈)
        expr <<= infixNotation(operand,
                               [
                                   (oneOf('+ -'), 1, opAssoc.RIGHT),      # 단항 연산자 (우측 결합)
                                   (oneOf('** ^'), 2, opAssoc.RIGHT),    # 지수 연산 (우측 결합)
                                   (oneOf('* /'), 2, opAssoc.LEFT),      # 곱셈/나눗셈 (좌측 결합)
                                   (oneOf('+ -'), 2, opAssoc.LEFT),      # 덧셈/뺄셈 (좌측 결합)
                               ])
        
        # 수식 파싱
        parsed_expression = expr.parseString(expression, parseAll=True).asList()
        
        # 추가 검증 단계: 연속된 단항 연산자가 있는지 확인
        if not validate_expression(parsed_expression[0]):
            raise ParseException("Invalid Syntax")
        
        return parsed_expression[0]
    except ParseException:
        return "Error: Invalid Syntax"

def validate_expression(expression):
    """
    중첩 리스트 형태의 수식을 재귀적으로 검사하여 연속된 단항 연산자가 있는지 확인합니다.
    단일 단항 연산자만 허용하고, 연속된 단항 연산자는 허용하지 않습니다.

    Args:
        expression (list or str): 파싱된 수식의 요소.

    Returns:
        bool: 유효한 수식이면 True, 그렇지 않으면 False.
    """
    if isinstance(expression, list):
        # 단항 연산자 두 개가 연속으로 사용된 경우 감지
        if len(expression) >= 2 and expression[0] in ('+', '-') and expression[1] in ('+', '-'):
            return False
        # 재귀적으로 모든 요소 검사
        for item in expression:
            if not validate_expression(item):
                return False
    return True

class MathExpressionCalculator:
    """
    수학 표현식을 계산하는 클래스.

    Attributes:
        operators (dict): 기본 연산자와 해당 연산을 수행하는 함수의 매핑.
        functions (dict): 수학 함수 이름과 해당 함수의 매핑.

    Methods:
        calculate_expression: 표현식을 계산.
        calculate_formula: 수식 문자열과 변수를 받아 계산 결과 반환.
    """
    # 기본 연산자 정의
    operators = {
        '+': np.add,
        '-': np.subtract,
        '*': np.multiply,
        '/': np.divide,
        '^': np.power,
        '**': np.power
    }
    
    # 기본 함수 정의
    functions = {
        'log10': np.log10,
        'ln': np.log,
        'exp': np.exp,
        'sqrt': np.sqrt,
        'abs': np.abs,
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
    }

    def __init__(self, custom_functions=None):
        """
        MathExpressionCalculator 초기화.

        Args:
            custom_functions (dict, optional): 추가적인 사용자 정의 함수들.
        """
        if custom_functions:
            self.functions.update(custom_functions)

    def calculate_expression(self, expression, variables):
        """
        주어진 표현식을 재귀적으로 계산합니다.

        Args:
            expression (list or str): 파싱된 수식의 요소.
            variables (dict): 변수명과 값을 매핑하는 사전.

        Returns:
            float or str: 계산 결과 또는 에러 메시지.
        """
        if isinstance(expression, str):
            if expression.startswith("Error:"):
                return expression  # 에러 메시지를 바로 반환
            # 숫자 처리: 부호, 소수점, 지수 표기법 지원
            if expression.replace('.', '', 1).replace('-', '', 1).isdigit() or \
               ('e' in expression.lower() and expression.replace('.', '', 1).replace('e', '').replace('-', '').isdigit()):
                return float(expression)
            # 변수 처리
            if expression in variables:
                return variables[expression]
            return "Error: Variable not found."  # 변수 미존재 시 에러 메시지 반환
        
        elif isinstance(expression, list):
            if len(expression) == 1:
                # 단일 요소인 경우 재귀적으로 계산
                return self.calculate_expression(expression[0], variables)
            
            elif len(expression) == 2:
                # 단항 연산자 처리 (+, -)
                if expression[0] in ('+', '-'):
                    operator = expression[0]
                    operand = self.calculate_expression(expression[1], variables)
                    if isinstance(operand, str) and operand.startswith("Error:"):
                        return operand  # 에러 메시지 전파
                    if operator == '+':
                        return +operand
                    elif operator == '-':
                        return -operand
                # 함수 처리
                elif isinstance(expression[0], str) and expression[0] in self.functions:
                    func_name = expression[0]
                    arg_expr = expression[1]
                    arg = self.calculate_expression(arg_expr, variables)
                    if isinstance(arg, str) and arg.startswith("Error:"):
                        return arg  # 에러 메시지 전파
                    func = self.functions[func_name]
                    try:
                        return func(arg)
                    except Exception as e:
                        return f"Error: {str(e)}"
                else:
                    return f"Error: Unknown function or operator '{expression[0]}'"
            
            elif len(expression) == 3:
                # 이항 연산자 처리
                left_expr, operator, right_expr = expression
                left = self.calculate_expression(left_expr, variables)
                if isinstance(left, str) and left.startswith("Error:"):
                    return left  # 에러 메시지 전파
                right = self.calculate_expression(right_expr, variables)
                if isinstance(right, str) and right.startswith("Error:"):
                    return right  # 에러 메시지 전파
                if operator in self.operators:
                    return self.perform_operation(left, operator, right)
                else:
                    return f"Error: Unsupported operator '{operator}'."
            
            else:
                # 긴 표현식 처리 (예: a + b + c + ...)
                result = self.calculate_expression(expression[0], variables)
                if isinstance(result, str) and result.startswith("Error:"):
                    return result  # 에러 메시지 전파
                i = 1
                while i < len(expression):
                    operator = expression[i]
                    next_expr = expression[i + 1]
                    next_value = self.calculate_expression(next_expr, variables)
                    if isinstance(next_value, str) and next_value.startswith("Error:"):
                        return next_value  # 에러 메시지 전파
                    if operator in self.operators:
                        result = self.perform_operation(result, operator, next_value)
                        if isinstance(result, str) and result.startswith("Error:"):
                            return result  # 에러 메시지 전파
                    else:
                        return f"Error: Unsupported operator '{operator}'."
                    i += 2
                return result
        else:
            return "Error: Unsupported expression format."

    def perform_operation(self, left, operator, right):
        """
        주어진 연산자와 피연산자를 사용하여 연산을 수행합니다.

        Args:
            left (float or np.ndarray): 왼쪽 피연산자.
            operator (str): 연산자.
            right (float or np.ndarray): 오른쪽 피연산자.

        Returns:
            float or np.ndarray or str: 연산 결과 또는 에러 메시지.
        """
        # 나눗셈 시 0으로 나누는 경우 처리
        if operator == '/':
            if isinstance(right, (int, float, np.ndarray)) and np.any(right == 0):
                return "Error: float division by zero"
        try:
            return self.operators[operator](left, right)
        except ZeroDivisionError:
            return "Error: float division by zero"
        except TypeError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def calculate_formula(self, formula, variables_dict=None, **variables):
        """
        주어진 수식 문자열과 변수를 받아 계산 결과를 반환합니다.

        Args:
            formula (str): 계산할 수식 문자열.
            variables_dict (dict, optional): 변수명과 값을 매핑하는 사전.
            **variables: 추가적인 변수 매핑.

        Returns:
            float or str: 계산 결과 또는 에러 메시지.
        """
        if variables_dict:
            variables.update(variables_dict)

        try:
            # 수식을 파싱
            expression = parse_math(formula)
            if isinstance(expression, str) and expression.startswith("Error:"):
                return expression  # 파싱 오류 메시지 반환
            # 표현식 계산
            result = self.calculate_expression(expression, variables)
            if isinstance(result, str) and result.startswith("Error:"):
                return result  # 계산 중 발생한 에러 메시지 반환
            return result
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    # 간단한 테스트 케이스
    calculator = MathExpressionCalculator()
    variables0 = {'a': 1.0, 'X1': 3.0, 'b': 2.0, 'X2': 4.0}
    
    # 다양한 방식으로 변수 전달하여 수식 계산
    print(calculator.calculate_formula('a * X1 + b / X2', a=1.0, X1=3.0, b=2.0, X2=4.0)) 
    print(calculator.calculate_formula('a * X1 + b / X2', variables_dict={'a': 1.0, 'X1': 3.0, 'b': 2.0, 'X2': 4.0})) 
    print(calculator.calculate_formula('a * X1 + b / X2', **variables0))
    
    # 배열과 함수를 포함한 복잡한 수식 계산
    calculator = MathExpressionCalculator()
    variables1 = {
        'a': 1.0,
        'b': 2.0,
        'c': 2,
        'd': 1,
        'e': 1,
        'o2': np.array([3.0, 3.1]),
        'o2_lag': np.array([4.0, 4.1]),
        'o2_lag2': np.array([4, 4.2])
    }
    print("결과:", calculator.calculate_formula('a * o2 + b / o2_lag + c * exp(o2_lag2 - d) + e', **variables1))
