---
layout: post
type: note
title: "Pin method"
description: "machine.Pin 클래스의 메서드에 대해서 설명하고 어떻게 사용하는지 자세하게 설명하였다."
date: 2026-07-20 21:51:00 +0900
category: AI-mobility
tags: [MicroPython, RP2040, GPIO]
---

# Pin method

## Pin method가 어떤 것들이 있는가?
우선 Pin 클래스의 생성과 파라미터는 다음과 같다.

```python
class machine.Pin(id, mode=-1, pull=-1, *, value=None, drive=0, alt=-1)
```

이에 대한 자세한 설명은 Pin class의 페이지를 살펴보기 바란다.

<a href="https://threetrue03.kro.kr/posts/Pin-Class/" target="_blank">
  Pin class 페이지로 이동
</a>

그렇게 Pin 클래스를 생성하였다면 메서드의 종류를 봐보자.

### value() - 핀의 값을 쓰거나 읽을 수 있다.

```python
핀객체.value([값])
```
value()는 인수를 넣었는지 안 넣었는지에 따라 쓰거나 읽을 수 있다.

#### 값을 넣었을 때 - 쓰기
값을 넣게 되면 해당 핀의 상태를 해당 값 상태로 바꿀 수 있다.

```python
led.value(1)
```

이면 HIGH 값을 쓰게 될 것이다.

#### 값을 넣지 않았을 때 - 읽기

```python
state = led.value()
```

값을 넣지 않으면 현재 핀의 논리 상태를 읽어 반환한다.

### on() - HIGH를 출력한다.

```python
led.on()
```

이 코드는 HIGH 값을 쓰는 value() 메서드와 같다.

```python
led.value(1)
```

### off() - LOW를 출력한다.

```python
led.off()
```

이 코드는 LOW 값을 쓰는 value() 메서드와 같다.

```python
led.value(0)
```

여기서 오해할 수 있는 점은, on(), off()가 장치를 키고 끄는 것으로 생각할 수 있다는 점이다.
장치를 키고 끄는 것이 아니라 해당 값을 1 또는 0으로 쓰는 것이다.

### toggle() - 현재 값을 반대로 쓸 수 있다.

```python
led.toggle()
```

현재 핀의 값을 반대로 바꾸는 것이다. HIGH면 LOW, LOW면 HIGH.
LED를 깜빡깜빡 거릴 때 사용하면 유용하다.

이는 다음 코드와 똑같다고 볼 수 있다.

```python
led.value(not led.value())
```

### init() - 핀의 설정을 다시 초기화할 수 있다.

```python
pin.init(mode, pull=None, value=None)
```

이미 만들어진 Pin 클래스의 IN, OUT을 변경하거나 pull의 업 또는 다운, 출력 초기값을 설정할 수 있다.

```python
pin = Pin(4, Pin.IN)

pin.init(Pin.OUT)
pin.value(1)
```

```python
led = Pin(25)
led.init(Pin.OUT, value=0)
```

### irq() - 핀 상태가 바뀔 때마다 함수를 실행시킬 수 있다.
irq는 Interrupt Request이고, 인터럽트가 발생했을 때 요청하는 메서드로 해석할 수 있다.

```python
irq(
    trigger=...,
    handler=...,
)
```

`handler`는 실행할 함수를 지정하는 것이다.
`trigger`는 함수가 실행될 조건을 지정할 수 있고 다음 두 가지로 확인해볼 수 있다.

- `Pin.IRQ_FALLING`: HIGH에서 LOW로 내려갈 때

```
IRQ_FALLING

3.3V ───┐
        └──── 0V
       이 순간 실행
```

- `Pin.IRQ_RISING`: LOW에서 HIGH로 올라갈 때

```
IRQ_RISING

0V ─────┐
        └──── 3.3V
       이 순간 실행
```
