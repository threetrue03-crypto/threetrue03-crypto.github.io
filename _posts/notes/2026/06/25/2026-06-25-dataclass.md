---
layout: post
title: "dataclass"
description: "dataclasses의 dataclass에 대해서 설명한다."
date: 2026-06-25
category: Python
tags: [Python, dataclasses, OOP]
---

# dataclass of dataclasses
## 목차
- [`dataclass란?`](#dataclass)
- [`__post_init__(self) 란?`](#post_init)
- [`번외, __doc__`](#doc)

<a id="dataclass"></a>
## ```dataclass```란?
```dataclass```는 데이터를 담기 위해 만든 클래스를 좀 더 편하게 담을 수 있게 해주는 라이브러리

```python
@classdata
class Student:
  ""이 클래스는 학생의 데이터를 저장하는 클래스입니다.""
  name: str
  age: int = 4
```

위 처럼 적으면 **def \_\_init__(...)** 를 만들어놓고 **self.name = ...** 하는 것보다 간결하고 가독성이 좋다.

<a id="post_init"></a>
## \_\_post\_init__(self) 란?
```dataclass```가 특별하게 알아보는 함수 이름이다.

```@dataclass```를 쓰면 파이썬이 자동으로 ```\_\_init__```을 만들어준다.
그런데, 클래스 안에 ```\_\_post\_init__```이 있으면, ```dataclass```는 다음과 같이 처리한다.

> "이 클래스는 ```\_\_post\_init__```이 있다. ```\_\_init__``` 이후에 자동으로 실행시켜야겠다."

```python
from dataclasses import dataclass

@dataclass
class A:
    x: int

    def __post_init__(self):
        print("객체 생성 완료 후 실행됨")
```
<a id="doc"></a>
## 번외, \_\_doc__
```dataclass``` 코드 예시에서 갑자기 문자열만 적어놓은 부분이 보인다.
```python
@classdata
class Student:
  ""이 클래스는 학생의 데이터를 저장하는 클래스입니다.""
  name: str
  age: int = 4
```

이것은 파이썬 기본 문법인, \_\_doc__ 속성이라고 하며 클래스 \_\_doc__ 와 함수 \_\_doc__ 로 나뉜다.
클래스 선언, 함수 선언 바로 아래 저렇게 문자열만 적어 놓고 .\_\_doc__ 로 접근할 수 있다.

```python
class A:
    """
    A 클래스 설명입니다.
    """

    x = 10

print(A.__doc__)
```
```python
def hello():
    """
    인사하는 함수입니다.
    """
    print("hi")

print(hello.__doc__)
```
