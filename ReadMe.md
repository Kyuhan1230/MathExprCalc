# Math Expression Calculator

이 프로젝트는 문자열 형태의 수학 표현식을 파싱하고 계산하는 기능을 제공합니다. 사용자는 복잡한 수학 표현식을 입력하고, 이를 계산하여 결과를 얻을 수 있습니다.

## 기능

- 수학 표현식 파싱
- 기본 수학 연산 (덧셈, 뺄셈, 곱셈, 나눗셈, 지수 연산)
- 고급 수학 함수 (로그(log10, ln), 삼각 함수, 제곱근, 절대값 등)

## 이 패키지를 사용해야 하는 이유
### 1. 맞춤 설정 가능
자신만의 함수를 추가하거나 기존 기능을 수정하여 개인적이거나 전문적인 요구에 맞게 조정할 수 있습니다. 이 패키지는 사용자가 특정 도메인이나 프로젝트에 필요한 맞춤형 수학 함수를 쉽게 추가하고 확장할 수 있도록 합니다. 

### 2. 교육적 가치
학습과 교육에 있어서 수학적 개념을 실습하고 탐구하는 데 유용한 도구입니다. 계산 과정을 통해 수학을 더 잘 이해할 수 있습니다.

### 3. 유연한 통합과 확장
웹 애플리케이션, 데스크톱 소프트웨어, 데이터 분석 도구 등 다양한 프로젝트에 이 패키지를 통합하여 확장된 수학적 기능을 쉽게 추가할 수 있습니다. 이를 통해 프로젝트의 범위를 넓히고, 사용자에게 더 많은 기능을 제공할 수 있습니다.

## 설치 방법

이 코드를 사용하기 위해서는 Python이 설치되어 있어야 하며, `pyparsing` 라이브러리가 필요합니다.

```bash
pip install pyparsing==3.0.7
```

## 사용 방법
먼저, math_expression_calculator.py 파일을 다운로드하고, 해당 파일을 프로젝트에 포함시킵니다.

### 기본 사용 예시
다음은 수학 표현식 계산기의 사용 방법에 대한 예시입니다:
```python
from math_expression_calculator import MathExpressionCalculator

calculator = MathExpressionCalculator()
result = calculator.calculate_formula("3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3", {})
print(result)
```

### 변수를 포함한 표현식 계산
변수를 포함하는 수식을 계산하려면, 변수의 값을 사전 형태로 전달해야 합니다:

```python
variables = {'x': 3, 'y': 4}
result = calculator.calculate_formula("x * 2 + y / 3", variables)
print(result)
```

### 테스트 방법
이 프로젝트에는 유닛 테스트가 포함되어 있어 코드의 정확성을 보장합니다. 테스트를 실행하려면 다음 단계를 따르세요:

1. unittest 모듈을 사용하여 테스트를 실행할 수 있습니다. 터미널에서 다음 명령어를 입력하여 테스트를 실행하세요:
```python
python -m unittest test_math_expression_calculator.py
```

2. 모든 테스트 케이스가 성공적으로 통과하면, OK라는 메시지가 출력됩니다.


## 문서
parse_math: 주어진 문자열에서 수식을 추출하는 함수입니다.

MathExpressionCalculator: 수학 표현식을 계산하는 클래스입니다.

calculate_formula: 문자열 형태의 수식과 변수 사전을 입력받아 결과를 계산합니다.

## 작성자
이름: 석규한

연락처: asdm159@gmail.com

## 라이선스
이 프로젝트는 MIT 라이선스에 따라 사용이 허가됩니다.