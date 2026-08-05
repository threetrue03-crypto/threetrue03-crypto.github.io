---
layout: post
type: note
title: "Modularization"
description: "파이썬 기본 문법인 모듈화의 대한 설명이다."
date: 2026-06-25
category: Python
tags: [Python, Module, Package]
---

# Modularization

## Modularization란?
> 코드를 기능별로 파일이나 클래스, 함수 단위로 분리해서 관리하는 것

**예를 들어**
모든 코드를 ```main.py``` 하나에 넣으면 이렇게 된다.
```
# main.py

# A코드
# B코드
# C코드
# D코드
...
```

Modularization을 통해서 역할 별로 나눠 ```main.py```의 코드 크기를 줄일 수 있다.
```
project/
├─ main.py
├─ current_alignment.py
├─ lyric_parser.py
├─ audio_player.py
└─ storage.py
```

## 어떻게 접근?
아래와 같이 되어 있다고 하자.
```
project/
├─ main.py
├─ current_alignment.py
├─ lyric_parser.py
├─ audio_player.py
└─ storage.py
```

그럼 main.py에서는 다음과 같이 접근할 수 있다.
```python
import current_alignment # 전체
from current_alignment import 특정클래스명, 특정함수명, 특정변수명 # 원하는 것만 가져오기
from current_alignment import Student, get_mean, ..., age # 여러 개 가져오기!
```
