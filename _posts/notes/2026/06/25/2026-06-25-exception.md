---
layout: post
type: note
title: "Exception"
description: "프로그램 실행 중 발생하는 오류 상황들을 정리하였다."
date: 2026-06-25
category: Python
tags: [Python, Exception Handling, Error]
---

# Exception

## Exception이란?
예외는 프로그램 실행 중에 발생하는 오류 상황을 의미한다.

> 파일이 없거나, 잘못된 값을 넣거나, 리스트 범위를 벗어난 인덱스를 접근하면 예외가 발생한다.

## Exceptions

| 예외                                                       | 의미                                         |
| :------------------------------------------------------- | :----------------------------------------- |
| <a href="#valueerror">`ValueError`</a>                   | 값은 들어왔지만 값의 내용이 잘못된 경우 사용한다.               |
| <a href="#typeerror">`TypeError`</a>                     | 값의 자료형이 잘못된 경우 사용한다.                       |
| <a href="#filenotfounderror">`FileNotFoundError`</a>     | 파일이나 폴더가 존재하지 않는 경우 사용한다.                  |
| <a href="#indexerror">`IndexError`</a>                   | 리스트, 튜플 등의 인덱스 범위를 벗어난 경우 발생한다.            |
| <a href="#keyerror">`KeyError`</a>                       | 딕셔너리에 존재하지 않는 key를 접근한 경우 발생한다.            |
| <a href="#zerodivisionerror">`ZeroDivisionError`</a>     | 숫자를 0으로 나누려고 할 때 발생한다.                     |
| <a href="#attributeerror">`AttributeError`</a>           | 객체에 존재하지 않는 속성이나 메서드를 사용한 경우 발생한다.         |
| <a href="#importerror">`ImportError`</a>                 | 모듈을 불러오지 못한 경우 발생한다.                       |
| <a href="#modulenotfounderror">`ModuleNotFoundError`</a> | 존재하지 않는 모듈을 import하려고 한 경우 발생한다.           |
| <a href="#permissionerror">`PermissionError`</a>         | 파일이나 폴더에 접근 권한이 없는 경우 발생한다.                |
| <a href="#runtimeerror">`RuntimeError`</a>               | 실행 중 일반적인 문제가 발생했지만 더 구체적인 예외가 애매할 때 사용한다. |
| <a href="#notimplementederror">`NotImplementedError`</a> | 아직 구현하지 않은 기능임을 표시할 때 사용한다.                |

---

<a id="valueerror"></a>

### `ValueError`

자료형은 맞지만 값 자체가 잘못된 경우 사용한다.

```python
interval_sec = -1

if interval_sec <= 0:
    raise ValueError("interval_sec은 0보다 커야 한다.")
```

위 코드에서 `interval_sec`은 숫자이므로 자료형은 맞다.

하지만 초 단위 간격이 `0` 이하이면 의미상 잘못된 값이다.

따라서 `ValueError`를 사용한다.

> 타입은 맞는데 값의 범위나 의미가 잘못되었을 때 사용한다.

---

<a id="typeerror"></a>

### `TypeError`

값의 자료형이 잘못된 경우 사용한다.

```python
interval_sec = "3"

if not isinstance(interval_sec, int):
    raise TypeError("interval_sec은 int 타입이어야 한다.")
```

위 코드에서 `"3"`은 숫자처럼 보이지만 실제로는 문자열이다.

함수에서는 정수를 기대하는데 문자열이 들어왔으므로 `TypeError`를 사용한다.

`ValueError`와의 차이는 다음과 같다.

```python
interval_sec = "3"   # TypeError 대상
interval_sec = -3    # ValueError 대상
```

> 타입 자체가 잘못되었으면 `TypeError`, 타입은 맞지만 값이 이상하면 `ValueError`를 사용한다.

---

<a id="filenotfounderror"></a>

### `FileNotFoundError`

파일이나 폴더가 존재하지 않는 경우 사용한다.

```python
from pathlib import Path

video_path = Path("video.mp4")

if not video_path.exists():
    raise FileNotFoundError(f"비디오 파일이 존재하지 않는다: {video_path}")
```

비디오 분석 프로그램에서는 입력 영상이 반드시 필요하다.

따라서 영상 파일이 없으면 더 진행하면 안 된다.

이럴 때 `FileNotFoundError`를 사용한다.

```python
from pathlib import Path

def extract_frames(video_path):
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"비디오 파일이 존재하지 않는다: {video_path}")

    print("프레임 추출을 시작한다.")
```

> 파일이 없으면 이후 코드가 정상적으로 실행될 수 없을 때 사용한다.

---

<a id="indexerror"></a>

### `IndexError`

리스트나 튜플에서 존재하지 않는 인덱스를 접근한 경우 발생한다.

```python
frames = ["frame1", "frame2"]

print(frames[5])
```

`frames`에는 인덱스 `0`, `1`만 존재한다.

그런데 `5`번 인덱스를 접근했으므로 `IndexError`가 발생한다.

직접 검사해서 예외를 발생시킬 수도 있다.

```python
frames = ["frame1", "frame2"]
index = 5

if index >= len(frames):
    raise IndexError("요청한 프레임 인덱스가 범위를 벗어났다.")

print(frames[index])
```

> 리스트, 튜플, 문자열처럼 순서가 있는 데이터에서 범위를 벗어난 위치를 접근할 때 발생한다.

---

<a id="keyerror"></a>

### `KeyError`

딕셔너리에 존재하지 않는 key를 접근한 경우 발생한다.

```python
song = {
    "title": "Butter",
    "bpm": 120
}

print(song["artist"])
```

`song` 딕셔너리에는 `"artist"`라는 key가 없다.

따라서 `KeyError`가 발생한다.

없는 key일 수도 있다면 `get()`을 사용할 수 있다.

```python
song = {
    "title": "Butter",
    "bpm": 120
}

artist = song.get("artist", "알 수 없음")
print(artist)
```

반드시 있어야 하는 key라면 직접 검사해서 예외를 발생시킬 수 있다.

```python
song = {
    "title": "Butter",
    "bpm": 120
}

if "artist" not in song:
    raise KeyError("song 딕셔너리에 artist 정보가 없다.")
```

> 딕셔너리에서 특정 key가 반드시 있어야 할 때 자주 확인한다.

---

<a id="zerodivisionerror"></a>

### `ZeroDivisionError`

숫자를 `0`으로 나누려고 할 때 발생한다.

```python
total_frames = 100
duration = 0

fps = total_frames / duration
```

수학적으로 `0`으로 나누는 것은 불가능하다.

따라서 `ZeroDivisionError`가 발생한다.

영상 처리에서는 영상 길이가 `0`이면 FPS나 진행률 계산이 불가능하다.

```python
total_frames = 100
duration = 0

if duration == 0:
    raise ZeroDivisionError("duration이 0이므로 fps를 계산할 수 없다.")

fps = total_frames / duration
```

> 나눗셈을 하기 전에 분모가 `0`인지 확인해야 한다.

---

<a id="attributeerror"></a>

### `AttributeError`

객체에 존재하지 않는 속성이나 메서드를 사용한 경우 발생한다.

```python
name = "video.mp4"

print(name.exists())
```

`exists()`는 `Path` 객체에서 사용할 수 있는 메서드다.

하지만 `name`은 문자열이므로 `exists()` 메서드가 없다.

따라서 `AttributeError`가 발생한다.

올바른 코드는 다음과 같다.

```python
from pathlib import Path

video_path = Path("video.mp4")
print(video_path.exists())
```

함수 안에서는 문자열로 들어온 경로를 `Path` 객체로 바꿔서 사용할 수 있다.

```python
from pathlib import Path

def check_video(video_path):
    video_path = Path(video_path)

    if not video_path.exists():
        raise FileNotFoundError(f"비디오 파일이 존재하지 않는다: {video_path}")
```

> 어떤 메서드를 쓰려면 그 메서드를 가진 객체인지 먼저 확인해야 한다.

---

<a id="importerror"></a>

### `ImportError`

모듈을 불러오는 과정에서 문제가 생긴 경우 발생한다.

모듈 자체는 존재하지만, 그 안에서 특정 기능을 불러오지 못할 때 발생할 수 있다.

```python
from math import not_exist_function
```

`math` 모듈은 존재하지만 `not_exist_function`은 존재하지 않는다.

따라서 `ImportError`가 발생한다.

선택적으로 기능을 불러오고 싶다면 다음처럼 처리할 수 있다.

```python
try:
    from math import not_exist_function
except ImportError:
    print("해당 기능을 불러올 수 없다.")
```

> 모듈을 불러오는 과정에서 문제가 생겼을 때 사용한다.

---

<a id="modulenotfounderror"></a>

### `ModuleNotFoundError`

존재하지 않거나 설치되지 않은 모듈을 import하려고 할 때 발생한다.

```python
import cv2
```

만약 `opencv-python`이 설치되어 있지 않으면 `ModuleNotFoundError`가 발생한다.

이 경우에는 패키지를 설치해야 한다.

```bash
pip install opencv-python
```

코드에서 직접 안내하려면 다음처럼 작성할 수 있다.

```python
try:
    import cv2
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "opencv-python이 설치되어 있지 않다. pip install opencv-python을 실행해야 한다."
    )
```

> 모듈 자체가 없거나 설치되지 않았을 때 발생한다.

---

<a id="permissionerror"></a>

### `PermissionError`

파일이나 폴더에 접근 권한이 없는 경우 발생한다.

```python
with open("protected_file.txt", "w") as f:
    f.write("hello")
```

해당 파일이 관리자 권한을 요구하거나 쓰기 권한이 없으면 `PermissionError`가 발생할 수 있다.

프로젝트에서는 결과 이미지를 저장할 폴더에 쓰기 권한이 없을 때 발생할 수 있다.

```python
output_path = "frames/frame_001.txt"

try:
    with open(output_path, "w") as f:
        f.write("frame data")
except PermissionError:
    print("파일을 저장할 권한이 없다.")
```

> 파일을 읽거나 쓰거나 삭제할 권한이 없을 때 발생한다.

---

<a id="runtimeerror"></a>

### `RuntimeError`

실행 중 문제가 발생했지만 더 적절한 예외가 애매할 때 사용한다.

```python
model = None

if model is None:
    raise RuntimeError("모델이 로드되지 않았다.")
```

예를 들어 악보 검출 모델이 준비되지 않았는데 검출을 실행하려고 하면 실행 상태가 잘못된 것이다.

```python
def detect_sheet(frame, model):
    if model is None:
        raise RuntimeError("악보 검출 모델이 로드되지 않았다.")

    print("악보 검출을 시작한다.")
```

다만 더 정확한 예외가 있다면 그 예외를 먼저 사용하는 것이 좋다.

```python
if not video_path.exists():
    raise FileNotFoundError("비디오 파일이 존재하지 않는다.")

if interval_sec <= 0:
    raise ValueError("interval_sec은 0보다 커야 한다.")
```

> 파일 문제, 타입 문제, 값 문제처럼 명확히 분류하기 어려운 실행 문제에서 사용한다.

---

<a id="notimplementederror"></a>

### `NotImplementedError`

아직 구현하지 않은 기능임을 표시할 때 사용한다.

```python
def detect_sheet_area(frame):
    raise NotImplementedError("악보 영역 검출 기능은 아직 구현되지 않았다.")
```

함수 이름과 구조는 먼저 만들어두고, 실제 구현은 나중에 할 때 사용한다.

```python
def detect_measure_change(prev_frame, current_frame):
    raise NotImplementedError("마디 전환 감지 기능은 아직 구현되지 않았다.")
```

이렇게 작성하면 해당 함수를 실수로 호출했을 때 아직 구현되지 않았다는 사실을 명확하게 알 수 있다.

> 나중에 구현할 함수의 자리만 먼저 만들어둘 때 사용한다.

---

## 상황별 예외 선택 기준

| 상황                      | 적절한 예외                |
| :---------------------- | :-------------------- |
| 타입이 잘못된 경우              | `TypeError`           |
| 타입은 맞지만 값이 잘못된 경우       | `ValueError`          |
| 파일이나 폴더가 없는 경우          | `FileNotFoundError`   |
| 리스트 인덱스가 범위를 벗어난 경우     | `IndexError`          |
| 딕셔너리에 없는 key를 접근한 경우    | `KeyError`            |
| 숫자를 0으로 나누는 경우          | `ZeroDivisionError`   |
| 객체에 없는 속성이나 메서드를 사용한 경우 | `AttributeError`      |
| 모듈을 불러오는 과정에서 문제가 생긴 경우 | `ImportError`         |
| 설치되지 않은 모듈을 import한 경우  | `ModuleNotFoundError` |
| 파일 접근 권한이 없는 경우         | `PermissionError`     |
| 실행 중 애매한 문제가 발생한 경우     | `RuntimeError`        |
| 아직 구현하지 않은 기능인 경우       | `NotImplementedError` |

---

## 프로젝트 코드 예시

```python
from pathlib import Path

def extract_frames(video_path: Path, interval_sec: int):
    if not isinstance(video_path, Path):
        raise TypeError("video_path는 Path 타입이어야 한다.")

    if not video_path.exists():
        raise FileNotFoundError(f"비디오 파일이 존재하지 않는다: {video_path}")

    if not isinstance(interval_sec, int):
        raise TypeError("interval_sec은 int 타입이어야 한다.")

    if interval_sec <= 0:
        raise ValueError("interval_sec은 0보다 커야 한다.")

    print("프레임 추출을 시작한다.")
```

위 코드의 예외 선택 기준은 다음과 같다.

| 코드                                  | 의미                     | 예외                  |
| :---------------------------------- | :--------------------- | :------------------ |
| `not isinstance(video_path, Path)`  | `video_path` 타입이 잘못됨   | `TypeError`         |
| `not video_path.exists()`           | 파일이 존재하지 않음            | `FileNotFoundError` |
| `not isinstance(interval_sec, int)` | `interval_sec` 타입이 잘못됨 | `TypeError`         |
| `interval_sec <= 0`                 | 값의 범위가 잘못됨             | `ValueError`        |
