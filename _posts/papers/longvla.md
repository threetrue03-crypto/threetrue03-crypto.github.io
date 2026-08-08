---
title: "Long-VLA: 로봇 조작을 위한 Vision-Language-Action 모델의 장기 지평 능력 확장"
date: 2026-08-04 14:37:00 +0900
description: "이동 단계와 상호작용 단계를 구분하는 단계 인지 입력 마스킹으로 VLA의 기술 연쇄 문제를 완화한 Long-VLA 논문 한국어 해석"
category: paper
tags: [robot-learning, VLA, long-horizon, skill-chaining, CALVIN]
---

# Long-VLA: 로봇 조작을 위한 Vision-Language-Action 모델의 장기 지평 능력 확장

> **원문 제목:** Long-VLA: Unleashing Long-Horizon Capability of Vision Language Action Model for Robot Manipulation  
> **저자:** Yiguo Fan, Pengxiang Ding, Shuanghao Bai, Xinyang Tong, Yuyang Zhu, Hongchao Lu, Fengqi Dai, Wei Zhao, Yang Liu, Siteng Huang, Zhaoxin Fan, Badong Chen, Donglin Wang  
> **소속:** Westlake University, Zhejiang University, Xi'an Jiaotong University, Beijing Advanced Innovation Center for Future Blockchain and Privacy Computing, University of Electronic Science and Technology of China  
> **학회:** 9th Conference on Robot Learning(CoRL 2025), Seoul, Korea  
> **프로젝트 페이지:** <https://long-vla.github.io>  
> **원문 PDF:** [longvla.pdf]({{ '/assets/papers/longvla/longvla.pdf' | relative_url }})  
> **번역 표기:** long-horizon은 **장기 지평**, skill chaining은 **기술 연쇄**, moving phase는 **이동 단계**, interaction phase는 **상호작용 단계**로 옮겼다.

<img src="{{ '/assets/papers/longvla/figure-1.png' | relative_url }}" alt="그림 1. Long-VLA와 기존 장기 지평 조작 접근법 비교" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 1. 기존 방법과 Long-VLA의 비교.** 기존의 통합 VLA는 짧은 과제에는 강하지만 기술 연쇄를 고려하지 못하고, 두 단계 방식은 이동과 상호작용을 별도 모델로 분리하여 확장성이 떨어진다. Long-VLA는 하나의 통합 모델을 유지하면서 단계 인지 입력 마스킹을 적용해 장기 지평 과제와 기술 연쇄를 함께 다룬다.

## 초록

Vision-Language-Action(VLA) 모델은 대규모 다중모달 데이터를 활용하여 강건하고 확장 가능한 로봇 정책을 학습하는 핵심 접근법으로 자리 잡았다. 그러나 기존 VLA 프레임워크는 대부분 짧은 시간 범위의 과제를 대상으로 하며, 여러 단계로 이루어진 장기 지평 로봇 조작에서는 **기술 연쇄**와 **하위 과제 간 의존성** 때문에 성능이 제한된다.

본 연구는 장기 지평 로봇 과제를 위해 특별히 설계된 최초의 종단간 VLA 모델인 **Long-VLA**를 제안한다. 핵심은 각 하위 과제를 이동 단계와 상호작용 단계로 나누고, 현재 단계와 관련된 감각 단서에 모델이 집중하도록 하는 **단계 인지 입력 마스킹**이다. 이 전략은 하위 과제 간 호환성을 높이면서도 VLA 학습의 확장성과 데이터 효율을 유지한다. 또한 특정 백본 구조에 종속되지 않아 기존 VLA에 핵심 구조 변경 없이 결합할 수 있다.

저자들은 장기 지평 조작을 체계적으로 평가하기 위해 **L-CALVIN** 벤치마크를 제안한다. 시뮬레이션과 실제 로봇 과제에서 Long-VLA는 기존 최고 성능 방법을 크게 앞서며 장기 지평 제어의 새로운 기준 성능을 제시한다.

## 1. 서론

VLA 모델은 시각 인식, 언어 이해, 행동 생성을 하나의 정책에 통합하고 대규모 로봇 데이터를 활용하여 범용 제어 능력을 학습한다. 하지만 대부분의 기존 VLA는 의미 공간과 행동 공간이 비교적 제한된 단일 또는 단기 과제를 중심으로 설계되어, 긴 순서의 하위 과제를 연속적으로 수행하는 문제는 충분히 해결하지 못했다.

최근의 주류 방법은 복잡한 과제를 여러 하위 과제로 나눈 뒤 각각을 별도의 지역 정책으로 처리한다. 이러한 분해는 개별 행동의 학습 난도를 낮추지만, 하위 과제 사이의 전환과 의존성을 명시적으로 모델링하지 못한다. 앞 단계의 작은 오차가 다음 단계의 초기 상태를 바꾸고 이후 오차를 누적시키는 현상이 바로 기술 연쇄 문제다.

온라인 미세조정, 보상 기반 실시간 보정, 입력 모달리티에 따른 계획과 실행의 분리 같은 방법도 제안되었다. 그러나 보상 기반 온라인 방식은 대규모 오프라인 학습을 사용하는 VLA와 잘 맞지 않고, 여러 모듈을 분리한 구조는 공동 종단간 학습을 방해한다. 따라서 VLA의 확장성과 데이터 효율을 유지하면서 장기 지평 기술 연쇄를 해결하는 일이 핵심 과제로 남아 있다.

Long-VLA는 각 하위 과제를 다음 두 단계로 구분한다.

1. **이동 단계:** 로봇이 목표 물체 또는 목표 위치로 접근한다.
2. **상호작용 단계:** 물체를 잡거나 누르거나 이동시키는 정밀 조작을 수행한다.

이동 단계에서는 정적 카메라의 3인칭 시점과 탐지 정보가 중요하고, 상호작용 단계에서는 그리퍼 카메라의 1인칭 시점이 중요하다. Long-VLA는 모달리티를 입력에서 제거하지 않고 어텐션 마스크만 바꾸어 단계별로 필요한 토큰을 선택한다. 따라서 입력 구조와 모델 구조를 그대로 유지하면서 모든 단계의 데이터를 하나의 정책으로 공동 학습할 수 있다.

본 연구의 주요 기여는 다음과 같다.

- 장기 지평 로봇 조작을 위한 통합 종단간 VLA 모델 Long-VLA를 제안한다.
- 이동·상호작용 단계에 맞춰 시각 토큰을 선택하는 단계 인지 입력 마스킹을 도입한다.
- 기존 CALVIN의 5단계 평가를 10단계로 확장한 L-CALVIN 벤치마크를 제안한다.
- 시뮬레이션과 실제 로봇 환경에서 장기 과제 길이가 길어질수록 더 큰 성능 향상을 보인다.

## 2. 관련 연구

### 2.1. Vision-Language-Action 모델

VLA는 시각 관측과 자연어 지시를 입력받아 로봇 행동을 직접 생성한다. 최근 연구는 더 크고 다양한 로봇 데이터셋을 활용한 사전학습으로 일반화 성능을 높이고 있다. 다만 현재의 VLA는 대체로 짧고 구조화된 과제에 맞춰져 있어, 하위 과제 간 상태 변화가 누적되는 장기 지평 상황에 대한 일반화가 부족하다.

### 2.2. 장기 지평 로봇 조작

전통적인 장기 조작 연구는 복잡한 과제를 하위 과제로 분해하고 각 하위 목표마다 별도의 정책을 사용한다. 그러나 각 정책이 독립적으로 학습되면 앞 단계의 최종 상태와 다음 단계가 학습한 초기 상태 사이에 불일치가 발생한다. 이를 해결하기 위한 연구는 크게 두 방향으로 나뉜다.

- 실행 도중 온라인 미세조정이나 보상 조절을 수행하여 오차 전파를 보정하는 방법
- 학습과 배포 사이의 입력 및 상태 분포 차이를 줄이는 방법

Plan-Seq-Learn은 이동 계획과 실행에 서로 다른 입력 모달리티를 사용해 기술 연쇄의 영향을 완화한다. 그러나 이러한 모듈식 방식은 VLA의 통합 종단간 학습과 충돌할 수 있다.

### 2.3. VLA에서의 장기 지평 조작

DexVLA와 같은 최근 VLA는 LLM을 이용해 과제를 하위 과제로 분해하여 학습 복잡도를 낮춘다. 하지만 기존 VLA 연구는 장기 실행 중 발생하는 기술 연쇄를 직접 다루지 않았다. Long-VLA는 별도의 정책을 여러 개 두지 않고, 입력 마스킹을 통해 한 정책이 이동과 상호작용을 모두 학습하도록 한다.

## 3. 방법

### 3.1. 분해 전략 재검토

저자들은 먼저 VLA에서 단계 분해가 실제로 필요한지 확인한다. 각 하위 과제를 이동 단계와 상호작용 단계로 더 세분화하고, 역기구학 대신 데이터로 학습한 이동 정책을 사용한다. 정확한 3차원 목표점이나 안정적인 역기구학 해를 얻기 어려운 실제 환경을 고려한 선택이다.

#### 분해 데이터 수집

CALVIN의 원래 궤적에서 64프레임 구간을 추출하고, 과제 탐지기가 완료 시점을 찾아 이동과 상호작용 구간을 나눈다. 물체 상태가 변하기 10~15프레임 전에 절단점을 설정하여 이동 단계의 끝과 상호작용 시작을 정렬한다. 이동 단계에는 물체와 위치를 반영한 별도의 이동 지시문을 추가하고, 상호작용 단계에는 CALVIN의 원래 지시문을 사용한다.

#### 분해 전략 예비 실험

| 방법 | 1개 | 2개 | 3개 | 4개 | 5개 |
|---|---:|---:|---:|---:|---:|
| MDT | 93.3 | 82.4 | 71.9 | 60.9 | 51.1 |
| MDT + 이동 정책 | 95.8 | 91.7 | 87.5 | 66.7 | 34.2 |

별도의 이동 정책을 추가하면 초반 및 중간 길이의 연속 과제 성능이 크게 개선된다. 이는 단계 분해 자체가 유효함을 보여준다. 다만 모델 두 개를 별도로 학습하는 방식은 확장성이 낮기 때문에, Long-VLA는 같은 아이디어를 하나의 통합 모델로 구현한다.

### 3.2. Long-VLA

#### 3.2.1. 학습 패러다임

<img src="{{ '/assets/papers/longvla/figure-2.png' | relative_url }}" alt="그림 2. Long-VLA의 데이터 분해, 단계 인지 마스킹, 종단간 학습" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 2. Long-VLA 전체 구조.** (a) 시각 관측과 언어 주석을 이동 단계와 상호작용 단계로 정렬한다. (b) 입력 구조를 바꾸지 않고 어텐션 계산에 참여할 토큰을 단계별로 선택한다. (c) 분해된 데이터를 하나의 VLA 정책으로 종단간 학습한다.

##### 데이터와 단계 분해

언어 지시가 붙은 하나의 궤적은 절단 시점 $d$를 기준으로 이동 단계와 상호작용 단계로 나뉜다.

$$
\tau=
\left\{
\left(s_t^{M},a_t^{M}\right)_{t\in[0,d]},
\left(s_t^{I},a_t^{I}\right)_{t\in[d+1,T]}
\right\}.
$$

여기서 $M$은 이동 단계, $I$는 상호작용 단계를 나타낸다. 기존 행동 표현에는 현재 단계를 알려주는 1차원 단계 식별자 $s_p$를 추가한다.

$$
a_t=
\left[
 x, y, z,
 eu_x, eu_y, eu_z,
 s_g, s_p
\right].
$$

$(x,y,z)$는 말단장치의 직교좌표, $(eu_x,eu_y,eu_z)$는 오일러각 기반 자세, $s_g$는 그리퍼의 열림·닫힘 상태다. 이동 단계에서는 $s_p=-1$, 상호작용 단계에서는 $s_p=1$로 설정한다. 추론 시작 시에는 $s_p=-1$로 초기화한다.

##### 마스킹을 이용한 입력 수준 적응

이동 단계에서는 그리퍼 카메라가 목표까지의 전역 이동 경로를 파악하는 데 제한적인 반면, 정적 카메라와 탐지 정보가 물체 위치를 찾는 데 유용하다. 상호작용 단계에서는 그리퍼 카메라가 정밀한 접촉과 조작에 유리하며, 불필요한 3인칭 배경은 시각 분포 변화를 키울 수 있다.

각 입력 토큰에 이진 마스크 $m_i\in\{0,1\}$를 할당한다. $m_i=1$이면 해당 토큰이 어텐션에 참여하고, $m_i=0$이면 제외된다. 토큰 마스크는 다음 어텐션 마스크로 확장된다.

$$
M_{ij}=m_i m_j.
$$

쿼리-키 유사도 행렬은 다음과 같다.

$$
P=\frac{QK^{\mathsf T}}{\sqrt{C}}.
$$

마스킹된 어텐션 가중치는 다음과 같이 계산된다.

$$
A_{ij}
=
\frac{
\exp(P_{ij})M_{ij}
}{
\displaystyle\sum_{k=1}^{N}\exp(P_{ik})M_{ik}
},
\qquad 1\le i,j\le N.
\tag{1}
$$

이 방식은 입력 모달리티를 물리적으로 제거하지 않는다. 따라서 단계가 바뀌어도 입력 텐서 구조는 동일하고, 하나의 모델에서 이동·상호작용 데이터를 함께 학습할 수 있다.

##### 학습 손실

행동 생성에는 조건부 확산 모델을 사용한다. 분해 데이터의 두 단계를 하나의 score matching 손실로 공동 감독한다.

$$
\mathcal{L}_{\mathrm{Diff}}
=
\mathbb{E}_{a\sim p_{\mathrm{data}}}
\mathbb{E}_{\eta\sim\mathcal{N}(0,\sigma_t^2 I)}
\left[
\left\|
D_{\theta}(\widetilde a_t,e_{\mathrm{post}},\sigma_t)-a_t
\right\|_2^2
\right].
\tag{2}
$$

시각 목표가 언어 지시와 의미적으로 일치하도록 InfoNCE 기반 목표 정렬 손실 $\mathcal L_{\mathrm{Goal}}$도 사용한다. 전체 손실은 다음과 같다.

$$
\mathcal{L}
=
\mathcal{L}_{\mathrm{Diff}}
+\alpha\mathcal{L}_{\mathrm{Goal}},
\qquad \alpha=0.1.
\tag{3}
$$

#### 3.2.2. 모델 구조

Long-VLA 정책 $\pi_\theta(a^t\mid s^t,d^t,g)$는 현재 관측 $s^t$, 탐지 입력 $d^t$, 잠재 목표 $g$를 조건으로 행동 $a^t$를 예측한다.

- **관측 인코더:** 그리퍼 카메라와 정적 카메라 영상을 학습 가능한 ResNet-18로 임베딩한다.
- **목표 인코더:** 언어가 있으면 언어 지시를, 언어가 없는 play 데이터에서는 미래 관측을 시각 목표로 사용한다. 두 목표는 동결된 CLIP의 텍스트·이미지 인코더로 변환한다.
- **탐지 통합:** CALVIN 일부 데이터로 Grounding DINO를 LoRA 미세조정하여 언어 조건부 물체 경계 상자를 얻는다. 탐지 특징은 FiLM으로 정적 카메라 특징을 조절한다.
- **다중모달 인코더:** GPT-2 계열 Transformer가 모든 모달리티 특징을 잠재 지각 토큰으로 통합한다.
- **행동 디코더:** 조건부 확산 모델이 가우시안 잡음에서 행동을 점진적으로 복원하며 DDIM으로 역과정을 수행한다.

DDIM 갱신은 논문의 표기를 따르면 다음 형태다.

$$
x_{t-1}
=
\frac{\sigma_{t-1}}{\sigma_t}x_t
-
\left(e^{-h}-1\right)e^{-\lambda_t}\widehat{x}_0.
$$

확산 디코더의 출력은 GELU를 사용하는 2층 MLP를 거쳐 최종 행동 벡터로 변환된다.

## 4. 실험

### 4.1. 실험 설정

<img src="{{ '/assets/papers/longvla/figure-3.png' | relative_url }}" alt="그림 3. 실제 로봇 실험 환경" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 3. 실제 로봇 실험 환경.** UR5e 로봇 팔, 외부 RealSense 카메라, 그리퍼 카메라를 사용한다. 실제 환경에서는 C-O-R-L 순서로 큐브를 그릇에 넣는 8단계 정렬 과제와 버튼 누르기·옥수수 잡기·싱크대에 넣기 등이 포함된 4단계 주방 정리 과제를 평가한다.

시뮬레이션은 CALVIN을 사용한다. 저자들은 기존 최대 5단계 평가를 10단계로 확장한 L-CALVIN을 구축하였다. 실제 환경에서는 다음 두 과제를 사용한다.

- **정렬:** C, O, R, L 큐브를 순서대로 집어 그릇에 넣는 8단계 과제
- **주방 정리:** 파란 버튼 누르기, 옥수수 잡기, 싱크대에 넣기, 노란 버튼 누르기의 4단계 과제

기본 정책은 다중모달 목표를 효율적으로 처리하고 비주석 play 데이터를 활용할 수 있는 MDT다. 추가 비교 대상으로 GR-1, UP-VLA, RoboVLMs, VLAS, OpenVLA, $\pi_0$를 사용한다.

### 4.2. 기본 정책과의 비교

#### L-CALVIN 시뮬레이션

<img src="{{ '/assets/papers/longvla/figure-4.png' | relative_url }}" alt="그림 4. L-CALVIN 시뮬레이션 성능" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 4. L-CALVIN 성능.** 동일 장면 D에서 학습·평가하는 D→D와, A·B·C·D 장면에서 학습하고 D에서 평가하는 ABCD→D 모두에서 Long-VLA가 기본 정책을 앞선다. 과제 길이가 길수록 상대 성능 향상이 커진다.

##### D→D: 순서상 완료율 1~5

| 방법 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| 기본 정책 | 0.86 | 0.64 | 0.53 | 0.47 | 0.37 |
| **Long-VLA** | **0.92** | **0.74** | **0.65** | **0.50** | **0.43** |

##### D→D: 순서상 완료율 6~10

| 방법 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|
| 기본 정책 | 0.31 | 0.28 | 0.21 | 0.13 | 0.11 |
| **Long-VLA** | **0.39** | **0.36** | **0.30** | **0.26** | **0.20** |

##### ABCD→D: 순서상 완료율 1~5

| 방법 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| 기본 정책 | 1.00 | 0.95 | 0.93 | 0.86 | 0.82 |
| **Long-VLA** | **1.00** | **1.00** | **0.98** | **0.91** | **0.85** |

##### ABCD→D: 순서상 완료율 6~10

| 방법 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|
| 기본 정책 | 0.75 | 0.68 | 0.61 | 0.53 | 0.45 |
| **Long-VLA** | **0.82** | **0.79** | **0.70** | **0.63** | **0.56** |

#### 실제 환경: 정렬

<img src="{{ '/assets/papers/longvla/figure-5.png' | relative_url }}" alt="그림 5. 실제 정렬 과제 성능" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 5. 실제 정렬 과제.** 목표 위치, 조명, 시각 방해 요소를 학습 때 보지 못한 형태로 바꾼다. 기본 정책은 긴 순서에서 성공률이 0으로 떨어지지만, Long-VLA는 8번째 과제까지 성공 가능성을 유지한다.

##### 무작위 위치

| 방법 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 기본 정책 | 0.70 | 0.60 | 0.40 | 0.35 | 0.20 | 0.05 | 0.00 | 0.00 |
| **Long-VLA** | **0.95** | **0.95** | **0.85** | **0.80** | **0.50** | **0.50** | **0.50** | **0.45** |

##### 보지 못한 조명

| 방법 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 기본 정책 | 0.50 | 0.40 | 0.35 | 0.30 | 0.15 | 0.05 | 0.00 | 0.00 |
| **Long-VLA** | **0.80** | **0.75** | **0.65** | **0.55** | **0.45** | **0.30** | **0.30** | **0.25** |

##### 시각 방해 요소

| 방법 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 기본 정책 | 0.55 | 0.45 | 0.25 | 0.20 | 0.05 | 0.00 | 0.00 | 0.00 |
| **Long-VLA** | **0.85** | **0.80** | **0.70** | **0.65** | **0.50** | **0.45** | **0.40** | **0.35** |

#### 실제 환경: 주방 정리

<img src="{{ '/assets/papers/longvla/figure-6.png' | relative_url }}" alt="그림 6. 실제 주방 정리 과제 성능" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 6. 주방 정리 과제.** 누르기, 잡기, 놓기 등 다양한 행동과 복잡한 배경을 포함한다. Long-VLA는 위치 변화, 조명 변화, 시각 방해 조건 모두에서 기본 정책보다 큰 폭으로 개선되며, 복잡한 환경일수록 상대 향상이 더 크다.

| 조건 | 방법 | 1단계 | 2단계 | 3단계 | 4단계 |
|---|---|---:|---:|---:|---:|
| 무작위 위치 | 기본 정책 | 12/20 | 8/20 | 5/20 | 3/20 |
| 무작위 위치 | **Long-VLA** | **18/20** | **14/20** | **13/20** | **11/20** |
| 보지 못한 조명 | 기본 정책 | 9/20 | 6/20 | 5/20 | 2/20 |
| 보지 못한 조명 | **Long-VLA** | **16/20** | **13/20** | **12/20** | **9/20** |
| 시각 방해 요소 | 기본 정책 | 11/20 | 7/20 | 6/20 | 3/20 |
| 시각 방해 요소 | **Long-VLA** | **17/20** | **13/20** | **12/20** | **11/20** |

### 4.3. 최고 성능 방법과의 비교

L-CALVIN D→D에서 Long-VLA는 GR-1과 RoboVLMs보다 높은 순차 완료율과 평균 완료 길이를 기록한다.

##### 순서상 완료율 1~5

| 방법 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| GR-1 | 0.83 | 0.58 | 0.48 | 0.35 | 0.24 |
| RoboVLMs | 0.81 | 0.60 | 0.44 | 0.34 | 0.28 |
| **Long-VLA** | **0.92** | **0.74** | **0.65** | **0.50** | **0.43** |

##### 순서상 완료율 6~10 및 평균 길이

| 방법 | 6 | 7 | 8 | 9 | 10 | 평균 길이 |
|---|---:|---:|---:|---:|---:|---:|
| GR-1 | 0.17 | 0.13 | 0.09 | 0.05 | 0.04 | 2.96 |
| RoboVLMs | 0.15 | 0.10 | 0.08 | 0.05 | 0.03 | 2.88 |
| **Long-VLA** | **0.39** | **0.36** | **0.30** | **0.26** | **0.20** | **4.75** |

<img src="{{ '/assets/papers/longvla/figure-7.png' | relative_url }}" alt="그림 7. 실제 환경에서 최고 성능 방법과 비교" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 7. 실제 환경 비교.** 주방 정리와 정렬 과제 모두에서 Long-VLA가 비교 모델보다 긴 행동 순서를 안정적으로 유지한다. 단일 단계의 기본 능력뿐 아니라 오류 누적을 억제하는 장기 지평 전략이 전체 성능을 결정한다.

### 4.4. 제거 실험

저자들은 분해 전략, 입력 수준 적응, 통합 모델의 기여를 분리해 분석한다. 표의 값은 완료한 평균 과제 길이다.

| 분해 | 입력 적응 | 통합 모델 | 실제 정렬 | 실제 주방 정리 | 시뮬레이션 D→D |
|---:|---:|---:|---:|---:|---:|
| ✗ | ✗ | ✓ | 2.3 | 1.4 | 4.11 |
| ✓ | ✗ | ✓ | 3.6 | 1.7 | 4.42 |
| ✓ | ✓ | ✗ | 4.1 | 2.0 | 4.76 |
| **✓** | **✓** | **✓** | **5.5** | **2.8** | **4.81** |

- **분해 전략:** 앞 단계의 불완전한 실행으로 초기 상태가 달라져도, 최신 장면 정보를 이용해 이동을 다시 정렬할 수 있다.
- **입력 수준 적응:** 이동 단계의 탐지·3인칭 시점과 상호작용 단계의 그리퍼 시점을 선택하여 일반화와 강건성을 높인다.
- **통합 모델:** 마스킹을 사용하면 단계별 입력 선택과 공동 종단간 학습을 동시에 유지할 수 있어 가장 높은 성능을 얻는다.

### 4.5. Long-VLA 패러다임의 확장성

Long-VLA는 MDT뿐 아니라 HULC에도 적용된다.

| 백본 | 기본 정책 평균 길이 | Long-VLA 평균 길이 | 향상 |
|---|---:|---:|---:|
| HULC | 2.65 | 3.30 | +0.65 |
| MDT | 4.11 | 4.81 | +0.70 |

서로 다른 VLA 백본에서 일관된 향상을 보인다는 점은 Long-VLA가 특정 구조에 종속되지 않는 입력 수준 모듈임을 뒷받침한다.

## 5. 결론

Long-VLA는 장기 지평 로봇 조작에서 지속적으로 발생하는 기술 연쇄 문제를 단계 인지 입력 적응으로 해결한다. 각 하위 과제를 이동과 상호작용으로 나누고, 단계별로 관련 있는 시각 토큰만 어텐션에 참여시켜 상태 분포 변화와 하위 과제 간 불일치를 완화한다.

이 방식은 여러 정책을 별도로 학습하지 않고 하나의 VLA 모델 안에서 종단간 학습을 유지한다. L-CALVIN과 실제 환경 실험에서 Long-VLA는 기존 최고 성능 방법보다 높은 성능을 보였고, 과제 순서가 길어질수록 상대적인 장점이 커졌다. 또한 백본 구조와 독립적으로 적용할 수 있어 다양한 VLA에 통합할 수 있다.

## 한계

- 이동 단계와 상호작용 단계를 나누는 학습 데이터 구축에는 여전히 수작업이 필요하다. 저자들은 향후 VLM을 이용해 자동화할 수 있다고 본다.
- 평가한 장기 지평 과제의 종류와 순서 길이가 아직 제한적이다.
- Long-VLA는 하위 과제의 초기 상태 불일치를 줄이지만, 정밀한 초기 조건에서도 발생하는 실제 실행 실패 자체를 복구하는 온라인 메커니즘은 포함하지 않는다.
- 더 다양한 VLA 구조와 로봇 형태에서의 전이 가능성을 추가로 검증해야 한다.

## 감사의 글

본 연구는 National Science and Technology Innovation 2030 Major Project(2022ZD0208800), NSFC General Program(62176215), National Natural Science Foundation of China(U21A20485), Xi'an Jiaotong University Fundamental Research Funds(xzy022024012)의 지원을 받았다.

# 부록

## A. 사전 정의

### A.1. VLA 모델의 정의

언어 조건 모방학습은 $N$개의 궤적 데이터로부터 로봇 행동을 학습한다. 하나의 궤적은 상태-행동 쌍의 순서다.

$$
\tau=\left\{(s_t,a_t)\right\}_{t=0}^{T}.
$$

궤적과 언어 지시의 데이터셋을 $\mathcal D=\{(\tau_i,l_i)\}_{i=1}^{N}$라 하면 표준 모방학습 목적함수는 다음과 같이 행동의 조건부 로그우도를 최대화한다.

$$
\mathcal{L}
=
\mathbb{E}_{(\tau,l)\sim\mathcal D}
\left[
-\sum_{t=0}^{T(\tau)}
\log \pi_\theta(a_t\mid s_t,l)
\right].
\tag{4}
$$

정책은 현재 상태와 언어 지시를 행동 공간으로 사상한다.

$$
\pi_\theta(a\mid s,l):
\mathcal S\times\mathcal L\rightarrow\mathcal A.
\tag{5}
$$

<img src="{{ '/assets/papers/longvla/figure-8.png' | relative_url }}" alt="그림 8. VLA 모델 정의" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 8. VLA 모델.** 언어 지시와 현재 환경 상태를 토큰화하고, 조건에 맞는 행동 시퀀스를 생성한다.

### A.2. 장기 지평 과제의 기술 연쇄 문제

<img src="{{ '/assets/papers/longvla/figure-9.png' | relative_url }}" alt="그림 9. 독립 실행과 연속 실행에서의 기술 연쇄 문제" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 9. 상태 불일치 분석.** 독립 실행에서는 각 하위 과제가 학습 분포와 가까운 초기 상태에서 시작한다. 연속 실행에서는 앞 단계의 최종 상태가 다음 단계의 초기 상태가 되어 위치와 자세가 달라진다. 이전 과제의 간섭을 제거해도 연속 실행 시 단일 과제 성능이 낮아지는 결과는 상태 불일치가 기술 연쇄의 주요 원인임을 보여준다.

## B. L-CALVIN

### B.1. 동기와 설계

CALVIN은 언어 조건 장기 조작을 평가하기 위해 다섯 하위 과제를 연속 실행한다. A, B, C, D의 네 장면 분할과 34개 개별 과제를 제공하지만, 34개 과제가 11개의 상위 범주로 묶여 있어 같은 범주의 과제를 한 순서에 중복 배치하지 않는다. 이 제약과 사후 검증 방식 때문에 긴 순서를 효율적으로 생성하기 어렵다.

L-CALVIN은 연속 과제 길이를 5개에서 10개로 늘리고, 34개 과제를 각각 독립 범주로 취급한다. 실행 가능한 다음 과제를 현재 상태에서 순차적으로 선택하므로 긴 시퀀스를 만든 뒤 다시 검증할 필요가 없다. 또한 모든 과제를 이동과 상호작용으로 분해한다.

### 이동·상호작용 지시문 예시

| 원 과제 | 이동 단계 지시 예시 | 상호작용 단계 지시 |
|---|---|---|
| 빨간 블록 오른쪽 회전 | 빨간 블록 위쪽으로 이동하라 | 빨간 블록을 잡고 오른쪽으로 회전하라 |
| 슬라이더 왼쪽 이동 | 오른쪽에서 슬라이더 손잡이로 접근하라 | 슬라이딩 문을 왼쪽으로 밀어라 |
| 서랍 열기 | 닫힌 서랍 앞 또는 손잡이로 이동하라 | 손잡이를 당겨 서랍을 열어라 |
| LED 켜기 | LED 버튼 위쪽으로 접근하라 | 버튼을 눌러 LED를 켜라 |

학습에서는 각 장면에서 64프레임 구간을 무작위로 추출하고 과제 탐지기로 완료 구간을 식별한다. 물체 상태가 변하기 10~15프레임 전에 절단점을 두어 시각적으로 자연스러운 단계 전환을 만든다. 34개 과제에 대해 총 372개의 고유 언어 지시를 구성하며, 검증에서는 학습 때 보지 못한 표현을 사용한다.

## C. 모델 세부사항

### C.1. 탐지 모듈

CALVIN 이미지 일부로 Grounding DINO의 Swin-OGC 변형을 LoRA 미세조정한다. 이동 단계의 정적 카메라 영상 $o_s$와 언어 질의 $l$이 주어지면 탐지 모델은 경계 상자를 예측한다.

$$
o_b=F_d(l,o_s).
\tag{6}
$$

경계 상자는 학습 가능한 위치 인코더 $\phi$로 잠재 특징에 투영된다.

$$
e_d=\phi(o_b).
\tag{7}
$$

탐지 특징은 두 개의 영 초기화 투영층을 사용하는 FiLM 방식으로 정적 카메라 특징 $e_s$를 조절한다.

$$
\widehat e_s
=
\left(1+W_{\mathrm{mul}}(e_d)\right)\odot e_s
+W_{\mathrm{add}}(e_d).
\tag{8}
$$

최종 다중모달 입력은 탐지로 보강된 정적 카메라, 그리퍼 카메라, 목표, 탐지 특징을 연결한다.

$$
e_{\mathrm{pre}}
=
\left[
\widehat e_s;
 e_g;
 e_{\mathrm{goal}};
 e_d
\right].
\tag{9}
$$

### C.2. 정렬 손실

이미지 목표 표현 $z_t^o$와 언어 목표 표현 $z_t^l$을 정렬하기 위해 코사인 유사도 $S(\cdot,\cdot)$를 사용하는 대조 손실을 적용한다. $\nu$는 온도, $B$는 배치 크기다. 아래 식은 원문의 표기를 유지하였다.

$$
\mathcal L_s
=
\left(1-\frac{1}{2B}\right)
\sum_{t=1}^{B}
\log
\left(
\frac{
\exp\left(S(z_t^o,z_t^l)/\nu\right)
}{
\displaystyle\sum_{n=1}^{B}
\exp\left(S(z_t^o,z_n^l)/\nu\right)
}
\right).
\tag{10}
$$

## D. 실험 세부사항

### D.1. 추가 비교 모델

- **GR-1:** 언어 조건 비디오 생성 사전학습 후 미래 프레임과 연속 행동을 공동 예측하는 GPT 계열 통합 Transformer
- **RoboVLMs:** 범용 VLM을 VLA 정책으로 변환하기 위한 백본·정책 헤드·시간 처리 설계 프레임워크
- **VLAS:** 음성, 이미지, 행동을 외부 음성 인식 없이 종단간 융합하고 사용자 지식을 위한 음성 검색 RAG를 추가한 VLA
- **$\pi_0$:** PaliGemma 백본과 flow matching 행동 전문가를 결합해 고주파 연속 행동 청크를 생성하는 cross-embodiment VLA

### D.2. 구현 세부사항

실제 실험은 UR5e 로봇 팔, 대각선 전방의 외부 카메라, 그리퍼 장착 카메라를 사용한다. 정렬과 주방 정리 과제마다 원격조작 시연 200개를 수집하고, 수집 중 이동·상호작용 단계 경계를 기록한다. 추가로 모든 실험 물체가 놓인 책상에서 약 2시간의 비주석 play 데이터를 수집한다.

L-CALVIN D→D 모델은 학습률 $10^{-4}$, 배치 크기 128로 40 epoch 학습하며 NVIDIA A100 80GB GPU 4장에서 약 18시간이 걸린다. 실제 환경은 과제별 모델을 800 epoch 학습하며 약 28시간이 걸린다.

### D.3. 성능 향상의 원인 분석

<img src="{{ '/assets/papers/longvla/figure-10.png' | relative_url }}" alt="그림 10. 기술 연쇄 중 위치, 조명, 방해 요소 변화에 대한 원인 분석" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 10. 원인 분석.** 정렬의 두 번째 단계와 주방 정리의 첫 번째 단계를 완료한 뒤, 다음 목표의 위치·조명·시각 방해 요소를 인위적으로 바꾼다. 기본 정책은 성공률이 크게 낮아지지만 Long-VLA는 약 80% 수준의 강건성을 유지한다. 이는 단계가 바뀔 때 입력을 다시 정렬하는 능력이 장기 지평 성능의 핵심임을 보여준다.

| 과제 | 조건 | 기본 정책 | Long-VLA |
|---|---|---:|---:|
| 정렬 기술 연쇄 | 위치 변화 | 12/20 | 15/20 |
| 정렬 기술 연쇄 | 조명 변화 | 8/20 | 17/20 |
| 정렬 기술 연쇄 | 시각 방해 | 14/20 | 17/20 |
| 주방 정리 기술 연쇄 | 위치 변화 | 10/20 | 14/20 |
| 주방 정리 기술 연쇄 | 조명 변화 | 8/20 | 18/20 |
| 주방 정리 기술 연쇄 | 시각 방해 | 13/20 | 17/20 |

### D.4. 입력 모달리티 제거 실험

$d$는 탐지 정보, $s$는 정적 카메라, $g$는 그리퍼 카메라를 뜻한다.

| 설정 | 이동 단계 | 상호작용 단계 | 평균 길이 |
|---|---|---|---:|
| 제안 단계 마스킹 | $d+s$ | $d+g$ | **4.81** |
| 분해만 사용 | $d+s$ | $d+s+g$ | 4.13 |
| 입력 수준 적응만 사용 | $d+s+g$ | $g$ | 4.66 |
| 통합 학습만 사용 | $s$ | $g$ | 3.65 |
| 모든 모달리티 사용 | $d+s+g$ | $d+s+g$ | 4.48 |

이동 단계에서 탐지와 정적 카메라를 사용하고, 상호작용 단계에서 탐지와 그리퍼 카메라를 사용하는 구성이 가장 높다.

### D.5. 학습 가능한 마스킹

단계 인지 마스킹을 고정 규칙이 아니라 학습 가능하게 만들어도 유사한 선택이 나타난다.

| 단계 | 정적 카메라 마스킹 | 그리퍼 카메라 마스킹 | 마스킹 없음 |
|---|---:|---:|---:|
| 이동 | 4.37% | **86.71%** | 8.91% |
| 상호작용 | **87.78%** | 2.68% | 9.54% |

이동 단계에서는 그리퍼 시점이 주로 가려지고, 상호작용 단계에서는 정적 시점이 주로 가려진다. 이는 저자들이 설계한 단계별 입력 선택과 일치한다.

### D.6. 추가 실험과 시각화

<img src="{{ '/assets/papers/longvla/figure-11.png' | relative_url }}" alt="그림 11. 보지 못한 조명과 시각 방해 조건의 추가 비교" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 11. 추가 실제 환경 비교.** 보지 못한 조명과 시각 방해 조건에서도 Long-VLA가 $\pi_0$보다 안정적인 장기 실행 성능을 보인다.

#### ABCD→D 추가 비교

##### 순서상 완료율 1~5

| 방법 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| VLAS | 0.88 | 0.80 | 0.72 | 0.58 | 0.49 |
| GR-1 | 0.92 | 0.81 | 0.71 | 0.63 | 0.58 |
| RoboVLMs | 0.90 | 0.80 | 0.78 | 0.70 | 0.64 |
| **Long-VLA** | **1.00** | **1.00** | **0.98** | **0.91** | **0.85** |

##### 순서상 완료율 6~10 및 평균 길이

| 방법 | 6 | 7 | 8 | 9 | 10 | 평균 길이 |
|---|---:|---:|---:|---:|---:|---:|
| VLAS | 0.46 | 0.34 | 0.28 | 0.29 | 0.16 | 5.00 |
| GR-1 | 0.54 | 0.50 | 0.40 | 0.30 | 0.29 | 5.68 |
| RoboVLMs | 0.60 | 0.51 | 0.41 | 0.36 | 0.34 | 6.04 |
| **Long-VLA** | **0.82** | **0.79** | **0.70** | **0.63** | **0.56** | **8.24** |

<img src="{{ '/assets/papers/longvla/figure-12.png' | relative_url }}" alt="그림 12. 비교 모델의 장기 정렬 실패 사례" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 12. 실패 사례.** 비교 모델은 큐브를 지정된 순서로 들지 못해 첫 과제를 다시 수행하는 오류를 보인다.

<img src="{{ '/assets/papers/longvla/figure-13.png' | relative_url }}" alt="그림 13. 주방 정리 과제 실행 비교" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 13. 주방 정리 실행 비교.** 기본 정책은 버튼 누르기에 실패하지만 Long-VLA는 파란 버튼 누르기, 옥수수 잡기, 싱크대에 넣기, 노란 버튼 누르기를 이어서 수행한다.

<img src="{{ '/assets/papers/longvla/figure-14.png' | relative_url }}" alt="그림 14. 정렬 과제 실행 비교" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 14. 정렬 실행 비교.** 기본 정책은 큐브 파지에서 실패하지만 Long-VLA는 C, O, R, L 큐브를 연속으로 집어 그릇에 넣는다.

<img src="{{ '/assets/papers/longvla/figure-15.png' | relative_url }}" alt="그림 15. L-CALVIN 10단계 롤아웃" style="display:block;max-width:100%;height:auto;margin:1.25rem auto;" />

**그림 15. L-CALVIN 10단계 롤아웃.** 이동 정책과 상호작용 정책의 전환 시점에 그리퍼 카메라 관측이 어떻게 사용되는지를 보여준다. 각 하위 과제 시작 상태를 안정적으로 만드는 것이 긴 순서를 완료하는 데 중요하다.

## 참고문헌

> 참고문헌은 논문 검색과 인용의 정확성을 위해 원문 표기를 유지하였다.


[1] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, et al. Openvla: An open-source vision-language-action model. In 8th Annual Conference on Robot Learning, 2024.

[2] J. Duan, W. Yuan, W. Pumacay, Y. R. Wang, K. Ehsani, D. Fox, and R. Krishna. Manipulate-anything: Automating real-world robots using vision-language models. In 8th Annual Conference on Robot Learning, 2024.

[3] M. Dalal, T. Chiruvolu, D. S. Chaplot, and R. Salakhutdinov. Plan-seq-learn: Language model guided rl for solving long horizon robotics tasks. In International Conference on Learning Representations, 2024.

[4] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. In Robotics: Science and Systems, 2023.

[5] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al. Rt2: Vision-language-action models transfer web knowledge to robotic control. In Conference on Robot Learning, pages 2165-2183. PMLR, 2023.

[6] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, et al. Octo: An open-source generalist robot policy. In Robotics: Science and Systems, 2024.

[7] H. Zhang, P. Ding, S. Lyu, Y. Peng, and D. Wang. Gevrm: Goal-expressive video generation model for robust visual manipulation. arXiv preprint arXiv:2502.09268, 2025.

[8] M. J. Kim, C. Finn, and P. Liang. Fine-tuning vision-language-action models: Optimizing speed and success, 2025. URL https: //arxiv.org/abs/2502. 19645.

[9] Y. Tian, S. Yang, J. Zeng, P. Wang, D. Lin, H. Dong, and J. Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation. In International Conference on Learning Representations, 2025.

[10] P. Ding, J. Ma, X. Tong, B. Zou, X. Luo, Y. Fan, T. Wang, H. Lu, P. Mo, J. Liu, et al. Humanoid-vla: Towards universal humanoid control with visual integration. arXiv preprint arXiv:2502.14795, 2025.

[11] W. Song, J. Chen, P. Ding, Y. Huang, H. Zhao, D. Wang, and H. Li. Ceed-vla: Consistency visionlanguage-action model with early-exit decoding, 2025. URL https: //arxiv. org/abs/2506. 13725.

[12] W. Zhao, G. Li, Z. Gong, P. Ding, H. Zhao, and D. Wang. Unveiling the potential of vision-languageaction models with open-ended multimodal instructions. 2025. URL https: //api.semanticscholar. org/Corpus ID : 278714573.

[13] Z. Gong, P. Ding, S. Lyu, S$. Huang, M. Sun, W. Zhao, Z. Fan, and D. Wang. Carp: Visuomotor policy learning via coarse-to-fine autoregressive prediction. ArXiv, abs/2412.06782, 2024. URL https ://api. semanticscholar.org/CorpusID: 274610389.

[14] S. Bai, W. Zhou, P. Ding, W. Zhao, D. Wang, and B. Chen. Rethinking latent representations in behavior cloning: An information bottleneck approach for robot manipulation. arXiv preprint arXiv:2502.02853, 2025.

[15] C. Cui, P. Ding, W. Song, S. Bai, X. Tong, Z. Ge, R. Suo, W. Zhou, Y. Liu, B. Jia, et al. Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation. arXiv preprint arXiv:2505,.03912, 2025.

[16] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky. ao: A vision-language-action flow model for general robot control, 2024. URL https: //arxiv.org/abs/2410.24164.

[17] J. Wen, Y. Zhu, J. Li, Z. Tang, C. Shen, and F. Feng. Dexvla: Vision-language model with plug-in diffusion expert for general robot control, 2025. URL https://arxiv. org/abs/2502.05855.

[18] G. Konidaris and A. Barto. Skill discovery in continuous reinforcement learning domains using skill chaining. Advances in neural information processing systems, 22, 2009.

[19] Z. Chen, Z. Ji, J. Huo, and Y. Gao. Scar: Refining skill chaining for long-horizon robotic manipulation via dual regularization. Advances in Neural Information Processing Systems, 37:111679-111714, 2024.

[20] Y. Lee, J. J. Lim, A. Anandkumar, and Y. Zhu. Adversarial skill chaining for long-horizon robot manipulation via terminal state regularization. In 5th Annual Conference on Robot Learning, 2021.

[21] Y. Chen, C. Wang, L. Fei-Fei, and K. Liu. Sequential dexterity: Chaining dexterous policies for longhorizon manipulation. In 7th Annual Conference on Robot Learning, 2023.

[22] M. Gramopadhye and D. Szafir. Generating executable action plans with environmentally-aware language models. In 2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 3568-3575. IEEE, 2023.

[23] X. Huang, D. Batra, A. Rai, and A. Szot. Skill transformer: A monolithic policy for mobile manipulation. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 10852-10862, 2023.

[24] U. A. Mishra, S. Xue, Y. Chen, and D. Xu. Generative skill chaining: Long-horizon skill planning with diffusion models. In Conference on Robot Learning, pages 2905-2925. PMLR, 2023.

[25] X. Li, M. Liu, H. Zhang, C. Yu, J. Xu, H. Wu, C. Cheang, Y. Jing, W. Zhang, H. Liu, et al. Vision-language foundation models as effective robot imitators. In International Conference on Learning Representations, 2024.

[26] J. Wen, Y. Zhu, J. Li, M. Zhu, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen, Y. Peng, et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. arXiv preprint arXiv:2409,125]4, 2024.

[27] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. Advances in Neural Information Processing Systems, 37:56619-56643, 2024.

[28] P. Ding, H. Zhao, W. Zhang, W. Song, M. Zhang, S. Huang, N. Yang, and D. Wang. Quar-vla: Visionlanguage-action model for quadruped robots. In European Conference on Computer Vision, pages 352367. Springer, 2024.

[29] X. Tong, P. Ding, D. Wang, W. Zhang, C. Cui, M. Sun, Y. Fan, H. Zhao, H. Zhang, Y. Dang, $. Huang, and S. Lyu. Quart-online: Latency-free large multimodal language model for quadruped robot learning. In EEE International Conference on Robotics and Automation, 2025.

[30] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation, 2025. URL https: //arxiv. org/abs/2410.07864.

[31] W. Zhao, P. Ding, M. Zhang, Z. Gong, S. Bai, H. Zhao, and D. Wang. Vlas: Vision-language-action model with speech instructions for customized robot manipulation. In International Conference on Learning Representations, 2025. 10

[32] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. arXiv preprint arXiv:2501.15830, 2025.

[33] W. Song, J. Chen, P. Ding, H. Zhao, W. Zhao, Z. Zhong, Z. Ge, J. Ma, and H. Li. Accelerating vision-language-action model integrated with action chunking via parallel decoding. arXiv preprint arXiv:2503.02310, 2025.

[34] H. Zhang, Z. Zhuang, H. Zhao, P. Ding, H. Lu, and D. Wang. Reinbot: Amplifying robot visuallanguage manipulation with reinforcement learning. 2025. URL https://api.semanticscholar. org/CorpusID : 278501320.

[35] H. Zhao, W. Song, D. Wang, X. Tong, P. Ding, X. Cheng, and Z. Ge. More: Unlocking scalability in reinforcement learning for quadruped vision-language-action models. ArXiv, abs/2503.08007, 2025. URL https: //api.semanticscholar.org/CorpusID : 276929414.

[36] W. Song, H. Zhao, P. Ding, C. Cui, S. Lyu, Y. Fan, and D. Wang. Germ: A generalist robotic model with mixture-of-experts for quadruped robot. 2024 [IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 11879-11886, 2024. URL https://api.semanticscholar.org/ Corpus ID :268536876.

[37] H. R. Walke, K. Black, T. Z. Zhao, Q. Vuong, C. Zheng, P. Hansen-Estruch, A. W. He, V. Myers, M. J. Kim, M. Du, et al. Bridgedata v2: A dataset for robot learning at scale. In Conference on Robot Learning, pages 1723-1736. PMLR, 2023.

[38] A. O'Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open xembodiment collaboration 0. In 2024 IEEE International Conference on Robotics and Automation (ICRA), pages 6892-6903. IEEE, 2024.

[39] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, §. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. In Robotics: Science and Systems, 2024.

[40] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. IEEE Robotics and Automation Letters, 7(3): 7327-7334, 2022.

[41] R. P. Paul. Robot manipulators: mathematics, programming, and control: the computer control of robot manipulators. Richard Paul, 1981.

[42] T. G. Dietterich. Hierarchical reinforcement learning with the maxq value function decomposition. Journal of artificial intelligence research, 13:227-303, 2000.

[43] C. Agia, T. Migimatsu, J. Wu, and J. Bohg. Stap: Sequencing task-agnostic policies. In 2023 [EEE International Conference on Robotics and Automation (ICRA), pages 7951-7958. IEEE, 2023.

[44] Z. Zhou, A. Garg, D. Fox, C. R. Garrett, and A. Mandlekar. Spire: Synergistic planning, imitation, and reinforcement learning for long-horizon manipulation. In 8th Annual Conference on Robot Learning, 2024.

[45] J. Zhang, J. Zhang, K. Pertsch, Z. Liu, X. Ren, M. Chang, S.-H. Sun, and J. Lim. Bootstrap your own skills: Learning to solve new tasks with large language model guidance. In Conference on Robot Learning, 2023.

[46] W. Liu, N. Nie, R. Zhang, J. Mao, and J. Wu. Learning compositional behaviors from demonstration and language. In 8th Annual Conference on Robot Learning, 2024.

[47] V. Myers, C. Zheng, O. Mees, K. Fang, and S. Levine. Policy adaptation via language optimization: Decomposing tasks for few-shot imitation. In 8th Annual Conference on Robot Learning, 2024.

[48] M. Dalal, M. Liu, W. Talbott, C. Chen, D. Pathak, J. Zhang, and R. Salakhutdinov. Local policies enable zero-shot long-horizon manipulation. In 2nd CoRL Workshop on Learning Effective Abstractions for Planning, 2024.

[49] X. Chen, W. Chen, D. Lee, Y. Ge, N. Rojas, and P. Kormushev. A backbone for long-horizon robot task understanding. IEEE Robotics and Automation Letters, 2025. 11

[50] G. Konidaris, S. Kuindersma, R. Grupen, and A. Barto. Robot learning from demonstration by constructing skill trees. The International Journal of Robotics Research, 31(3):360—375, 2012.

[51] M. Sun, P. Ding, W. Zhang, and D. Wang. Score-based diffusion policy compatible with reinforcement learning via optimal transport. ArXiv, abs/2502.12631, 2025. URL https://api.semanticscholar. org/Corpus ID :276421829.

[52] M. Reuss, Omer Erding Ya&Smurlu, F. Wenzel, and R. Lioutikov. Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. In Robotics: Science and Systems, 2024.

[53] K. He, X. Zhang, S. Ren, and J. Sun. Deep residual learning for image recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 770-778, 2016.

[54] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, et al. Learning transferable visual models from natural language supervision. In International conference on machine learning, pages 8748-8763. PmLR, 2021.

[55] S. Liu, Z. Zeng, T. Ren, F. Li, H. Zhang, J. Yang, Q. Jiang, C. Li, J. Yang, H. Su, et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. In European Conference on Computer Vision, pages 38-55. Springer, 2024.

[56] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, et al. Lora: Low-rank adaptation of large language models. International Conference on Learning Representations, 1(2):3, 2022.

[57] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville. Film: Visual reasoning with a general conditioning layer. In Proceedings of the AAAI conference on artificial intelligence, volume 32, 2018.

[58] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In The Twelfth International Conference on Learning Representations, 2024.

[59] J. Zhang, Y. Guo, Y. Hu, X. Chen, X. Zhu, and J. Chen. Up-vla: A unified understanding and prediction model for embodied agent, 2025.

[60] X. Li, P. Li, M. Liu, D. Wang, J. Liu, B. Kang, X. Ma, T. Kong, H. Zhang, and H. Liu. Towards generalist robot policies: What matters in building vision-language-action models. arXiv preprint arXiv:2412.14058, 2024.

[61] Z. Chen, Z. Shi, X. Lu, L. He, 8. Qian, Z. Yin, W. Ouyang, J. Shao, Y. Qiao, C. Lu, et al. Rh20t-p: A primitive-level robotic dataset towards composable generalization agents. arXiv preprint arXiv:2403.19622, 2024.

[62] O. Mees, L. Hermann, and W. Burgard. What matters in language conditioned robotic imitation learning over unstructured data. IEEE Robotics and Automation Letters (RA-L), 7(4):11205—11212, 2022. A Preliminaries A.1l_ Definition of VLA Models Imitation learning with language instructions enables an agent to learn manipulation actions from a dataset of N trajectories {r;}*,. Each trajectory r consists of a sequence of state-action pairs, rT = {(s;,a:)}2.9, where s; and a; denote the state and action at time step ¢, respectively. The learning objective follows the standard imitation learning paradigm [? ], which maximizes the loglikelihood of the demonstrated actions conditioned on states and language instructions: I7| L=EGaywp | S- log mo(arlse.1) | (4) t=0 where D = {(7,!);}4_, denotes the dataset of trajectory-instruction pairs. As illustrated in Figure 8, the policy 7» is modeled as a text-conditioned action predictor, mapping from the current state and language instruction to the action space: ma(als,l): Sx LA, (5) where S, £, and A denote the state, language instruction, and action spaces, respectively. Through optimizing 7, the agent learns to execute actions that align with both the observed states and the given language commands. Language Instruction (1) State(s) “Put the red block emg\) 1) og or cal into the drawer.” re cts Language Image (p41; 4142; --- At4n) Tokenizer Tokenizer G=0 \\ my Vision-Language-Action Model (9) I(d;| 1, Sz) A Figure 8: Definition of VLA Models. VLA models generate sequences of actions conditioned on input language instructions and the current environmental state. A.2 Skill Chain Challenges in Long-horizon Tasks As is shown in Figure 9, we verify the skill chain challenage also exits in current VLA models. In subfigure (b), we can see that even after removing the interference from previous tasks, the success rate for individual tasks still continues to decline. In subfigure (c), we further verify this point. We conducted a single-task test, allowing the model to be tested independently in both the Independent and Continuous environments. We found that once the tasks are performed continuously, the model’s single-task performance is lost. The above experimental analyses all demonstrate this issue. Task 1 Task 2 Task 5 S 100 Each Task Overall —e © ° ° — : * = —_ Turn on Lift pink block Opn 2” led slider drawer 3 G25 Initial Condition Final State woo a 1 2 3 4 5 Number of Tasks (b) Comparison between individual subtask and overall task Independent : . pe \ performance under the Continuous setting & 100 Continuous Independent a of a Continuous % 50 8uy ¥, ~. # wi 5 Rotating Pushing Lifting (a) Illustration of the Independent and Continuous (c) Comparison between Independent and Continuous settings execution settings across different tasks Figure 9: (a) Illustration of skill-chaining challenges like state mismatch in CALVIN benchmark. In the independent setting, each subtask starts from a state within the training distribution. In the continuous setting, subtasks are executed sequentially, causing potential distribution shifts. (b) The performance drop in individual subtasks suggests the potential impact of state mismatch. (c) Validates the effect of state mismatch (e.g., position differences) across different tasks. B- L-CALVIN B.1 L-CALVIN. Motivation of L-CALVIN. Improving the performance of long-horizon tasks is crucial for robotic systems operating in real-world environments, where robots must execute continuous and complex operations. In such settings, the quality of task execution at each stage directly influences subsequent Table 5: Language instruction examples for the movement and interaction phases. We extend the movement phase instructions to increase diversity, while retaining the original CALVIN instructions for the interaction phase. Task Type | rotate red block right move slider left open drawer turn on led move: move to the move: go to the slider move: move in front of | move: move to the top Movement red block from the top from the right the closed drawer side of the led button Instruction move: go to the top move: reach the the right move: go to the move: approach the led side of the red block side of slider handle drawer handle button from the top Interaction Take the red block and Push the sliding Pull the handle press the button to Instruction rotate it to the right door to the left side to open the drawer turn on the led light Algorithm 1 CALVIN Sequence Generation in Algorithm 2 L-CALVIN Sequence Generation original paper [40] Input: A: action sequence Input: A: action sequence Aset: action sequence set Aset: action sequence set S: current state S: start state len: sequence length len: sequence length Initialize: RandomPossibleNext(S) Initialize: CheckSequence(5, A) 1: Random S$ 1: Random A with len tasks 2: for i in range(len) do 2: if CheckSequence(S, A) then 3 if PossibleNext(.S) then 3: Aset.append(A) 4 N «+ RandomPossibleNext(S) 4: end if 5: A.append(N) 6: else 7 break 8 end if 9: end for 10: Aset.append(A) tasks, making long-horizon task planning and execution inherently more challenging than singletask assessments. Background of CALVIN. The CALVIN benchmark provides a long-horizon evaluation environment composed of sequences of five decomposed subtasks. It includes four different scene splits (A, B, C, D), with evaluations typically conducted in scene D. In CALVIN, 34 individual tasks are grouped into 11 major categories to generate random evaluation sequences, which limits the maximum sequence length to 11 tasks. Additionally, sequence generation follows a random sampling and verification process, which is both inefficient and unable to scale to longer horizons. Limitation of CALVIN. Existing evaluation protocols primarily focus on short temporal horizons, typically involving sequences of only five tasks. This limited scope fails to adequately capture the performance of robotic systems under more realistic, extended operation scenarios. When faced with longer task sequences, current models experience significant performance degradation, with different models’ performances eventually converging to similar levels, indicating a model-agnostic challenge. Overview of L-CALVIN Benchmark. To address this limitation, we introduce L-CALVIN, an extended version of the CALVIN benchmark. L-CALVIN increases the task sequence length from five to ten consecutive tasks, providing a more comprehensive benchmark for evaluating long-horizon task performance. This extended evaluation framework allows for a more rigorous examination of task execution consistency, adaptability, and long-term efficiency. L-CALVIN removes the categorybased constraint by treating all 34 tasks as independent categories, enabling the generation of sequences longer than ten tasks. Furthermore, each task execution is decomposed into two distinct phases: movement and interaction, as illustrated in Figure 15. By switching camera perspectives between phases, we enhance the agent’s semantic understanding and mitigate the state initialization gap between tasks. Sequence Generation. Corresponding to the L-CALVIN benchmark, we construct a phase-specific dataset to support policy learning under diverse language instructions. Using ground truth information from the CALVIN simulation, we re-annotate the dataset by decomposing trajectories based on object movement states. We introduce additional language instructions specifically for the movement phase, while keeping interaction phase instructions consistent with the original annotations. During validation, we use language expressions that differ from those seen during training to assess generalization. Examples of the augmented language instructions are presented in Table 5. For phase decomposition, we detect position changes of target objects between consecutive frames to segment movement and interaction phases. Compared to the random sequence generation approach of CALVIN (Algorithm 1), L-CALVIN adopts a structured generation method (Algorithm 2) that incrementally selects executable tasks, allowing efficient construction of longer sequences without post-validation. Overview of L-CALVIN Dataset. We randomly extract sequences with a window size of 64 frames. Each sequence 1s labeled if a task detector identifies task completion, following the approach in [40]. The associated language instruction is then augmented with a movement command using a manually designed template based on the identified object and location, while retaining the original instruction as the interaction phase. Based on the task prompt, we determine the cutting point to be 10 to 15 frames before the object’s state change to ensure coherent visual composition. In total, we retain language annotations for 34 tasks, resulting in 372 unique instructions. Comparison with CALVIN. The original CALVIN approach ensures that no two tasks from the same major category appear within a sequence; however, this constraint limits sequence length and reduces data generation efficiency. In contrast, L-CALVIN leverages a finer-grained categorization at the minor task level, significantly increasing the diversity of feasible sequences and approximately tripling the number of block manipulation tasks. This enhanced structure makes L-CALVIN particularly suited for evaluating long-horizon task execution under realistic and challenging conditions. C Model Details C.1 Detection Module Details To enable accurate object navigation and interaction in dynamic scenes, we incorporate additional detection information. Specifically, we select a subset of images from the CALVIN dataset and fine-tune Grounding DINO [55] (Swin-OGC variant) using LoRA [56]. The model, denoted as F;,, is trained to localize target objects based on language queries /. Given a third-person image o, from the movement phase, F;, outputs a set of bounding boxes: On = Fi (1, Os), (6) where 0, € R**4. This effectively transforms image-based object representations into finegrained, pixel-level spatial information. To align these spatial locations with the model’s latent representation, we apply a trainable positional encoding function ¢ to project the bounding boxes into the feature space: €, = (0p), ey € R2NOX4, (7) where e, represents the latent feature encoding of the detection boxes. We then integrate this detection-aware feature into the visual embedding e, of the static camera view using the FiLM mechanism [57]. This is achieved through two learnable projection matrices, Winu and Waa, initialized to zero for unbiased fusion: és = (1+ Waun(en)) © es + Waaa(en), (8) where © denotes element-wise multiplication. This formulation allows dynamic modulation of image features based on detection results. Finally, we construct the multimodal input embedding e,re for the transformer encoder by concatenating the goal feature e,,,;, the gripper camera observation encoding zg, the detection encoding ey, and the FiLM-enhanced static view é,: Epre = (és; 1€q3+€goals; ed): (9) C.2 Alignment Loss To align the image goal and language goal representations, we utilize a contrastive learning loss, which can be formulated as: 1.< exp (S(z?, 2})/v) Lo=(1- — lo. 10 _ ap) «(pe ene uo) where (-,-) denotes the cosine similarity, v is a temperature parameter, and B is batch size. D_ Experiment Details D.1_ Baseline. We conduct supplementary experiments with additional baseline models to facilitate a more comprehensive comparison of different types of models. * GR-1 [58]: A GPT-style unified transformer that leverages large-scale languageconditioned video generative pre-training and is then fine-tuned on robot data to jointly predict future frames and continuous actions, boosting CALVIN success to 94.9% and exhibiting strong zero-shot generalization to unseen scenes, objects, and real-world tasks. * RoboVLMs [60]:A flexible framework that turns off-the-shelf Vision—Language Models into VLA policies, systematically dissecting backbone selection, policy formulation (history-aware continuous actions with a policy head), and timing for cross-embodiment data. * VLAS [31]: An end-to-end VLA policy that fuses raw speech, images, and actions without an external automatic speech recognition, aligns speech inside LLaVA, and adds a voice-retrieval RAG for user-specific knowledge. * aq [16]: A cross-embodiment VLA model that augments a PaliGemma backbone with a flow-matching action expert to generate high-frequency continuous action chunks; pretrained on 10,000 h of diverse single- and dual-arm data and post-trained on curated demos. D.2 Implementation Details. Hardware of Real-world Experiments. As shown in Figure 3, we utilizes a URSe robotic arm within a real-world desktop environment, which includes bowls, cubes, corn, and a sink. We employ two cameras: one positioned diagonally in front of the robotic arm to provide an overhead view, and another mounted on the robot gripper for precise interactions with the objects. Real-world Play Dataset. We collected 200 demonstrations for each of the Sorting and Cleaning tasks via teleoperation. By pressing the ’m’ key, we performed data decomposition during collection. In the Sorting task, blocks were placed arbitrarily across the tabletop. For the Cleaning task, while constraining the buttons and sink so that they could only move along the front—back axis, the position of the corn was randomized on the tabletop. In addition, we gathered approximately two hours of unlabeled play data in which volunteers freely explored the tabletop arranged with all experimental objects. Detection Information. Since the CALVIN environment differs significantly from the object states in real-world scenarios, and the captured images have relatively low resolution, we fine-tune GroundingDINO within to obtain detection information. However, in real-world experiments, we zero-shot use GroundingDINO on images, with prompts related to the task target objects, such as “the corn” or “the blue button”. Training Details. For the L-CALVIN task, we train the DD model for 40 epochs using a learning rate of le-4 and a batch size of 128, taking approximately 18 hours on four NVIDIA A100 GPUs (80GB VRAM). For the real-world tasks, we train one model for each of the two tasks over 800 epochs, taking about 28 hours. Step 2 — ee ee Step 3 Step 1 —_ s Step 2 Put in the bowl Lift the O cube Press blue button Grab the corn Random Location | Random Location —_ Human Human Interference Interference of of Sorting New -<) Cleaning L> os “—> Method Success Rate (%) of Skill Chain in Sorting | Success Rate(%) of Skill Chain in Cleaning Location Lighting Distraction | Location Lighting Distraction Base Policy 12/20 8/20 14/20 10/20 8/20 13/20 L VLA 15/20 17/20 17/20 14/20 18/20 17/20 ong- (25% tT) (112% 7) (22% ft) (40% 7) (125% TF) (33% 7) Figure 10: Underlying Cause Analysis. D.3 Underlying Cause Analysis. To further investigate the factors underlying the observed performance improvements, we conducted a validation experiment, as illustrated in Figure 10. For the sorting task, after completing step 2 (putting the cube into the bowl), we deliberately introduced perturbations to the position of the next target object, scene illumination, and added visual distractors before evaluating the subsequent task. Similarly, for the cleaning task, we applied comparable augmentations after completing step 1 (pressing the button). These additional interferences, introduced after the completion of each preceding task, result in a suboptimal initial state for the subsequent task. This leads to significant performance degradation in the base policy, with success rates dropping by approximately 50%. In contrast, our proposed approach consistently maintains a success rate of around 80%, demonstrating strong robustness during the skill chaining phase. This robustness is a key reason why our model’s performance remains stable and does not experience significant drops in long-horizon tasks. Moreover, the performance improvement achieved by our method is generally more pronounced in the more challenging cleaning task compared to sorting, which aligns with the differences observed in Figure 5 and Figure 6. D.4_ Ablation on Input Modality Here, in Table 6, it is evident that using detection and third-person view in the Moving phase, and using detection and first-person view in the Interaction phase, constitutes the optimal configuration. D.5 Learable Masking Strategy. There are concerns that phase-aware masking may be less effective in complex tasks such as obstacle avoidance. Nevertheless, its strong performance on most tabletop and relatively simple tasks highlights its effectiveness in addressing the skill-chaining problem. For phase-based masking, we draw on conclusions from prior works such as Plan-Seq-Learn. Furthermore, by making the masking learnable, we observe that the moving stage tends to activate third-person views, while the interaction stage activates first-person views. As shown in Table 7, the outcome consistent with the design of our method. Table 6: Ablation on Input Modality on CALVIN(D-D). d denotes detection information, s denotes static camera views, g denotes gripper camera views. Setting | Moving | Interaction | Avg. Len t 1d s gi]d ies g\| 4 iv v ¥ 4.81 w Decomposition ¥ Vv vv 4.13 w Input-level Adaptation |“ “4% wv v 4.66 w Unified Training A ¥ 3.65 Yo v¥\|\% vv 4,48 Table 7: Rate of learnable masking in different phases. Phase | Masking | static masking | gripper masking | no masking Moving 4.37% 86.71% 8.91% Interaction 87.78% 2.68% 9.54% D.6 More Experiments. More Comparison of Long-VLA and zo. Here, we provide additional comparisons under unseen lighting conditions and visual distractions in Figure 11. Our Long-VLA also outperforms 7p in these more challenging, unseen scenarios. Pecfoamance in Unseen Lighting Performance in Unseen Lighting Logg¥LA E & Task completed (6) Task completed (%) # & 8 w & ' , 6 &€ # s o & @ Task completed(%) ‘Task completed (%) # # 8 & 8 © Visual Distraction 8B - = ‘ & # > es o Figure 11: More Comparison on Real World Scenarios (Left: Cleaning; Right: Sorting). More Comparison of Simulation Environment. Here, we also include additional comparisons on the ABCD-—D split of the L-CALVIN simulation benchmark in Table 8. More Visualization in Real-world Scenarios. Here, we offer more visualization in Figure 12, Figure 13 and Figure 14. More Visualization in Simulation Scenarios. Here, we offer more visualization in Figure 15. Table 8: Comparison with SOTA methods on L-CALVIN simulation benchmark. Tasks Completed in Sequence Train—Test Method Avg. Len 1 2 3 4 5 6 7 8 9 10 VLAS 0.88 0.80 0.72 0.58 0.49 046 0.34 0.28 0.29 0.16 5.00 ABCD-3D GR-1 0.92 0.81 0.71 0.63 0.58 0.54 0.50 0.40 0.30 0.29 5.68 RoboVLMs 0.90 0.80 0.78 0.70 0.64 0.60 0.51 0.41 0.36 0.34 6.04 Long-VLA_ 1.00 1.00 0.98 0.91 0.85 0.82 0.79 0.70 0.63 0.56 8.24 Cubes are not lift in order Re-did the |_| first task Fail to press the button LongVLA Press blue button Grab the corn Put in the sink Press yellow button Figure 13: Comparison of Execution in Sorting Task Lift the C cube LongVLA | Put in the bow! Put in the bowl Lift the L cube Put in the bowl Figure 14: Comparison of Execution in Cleaning Task rotate_blue_block_left ; “move to the blue block”, “take the blue block and rotate it to the left” BAGELS push_red_block_right : “move to the red block”, “go push the red block right” close_drawer: “move towards the open drawer”,*. “push the handle to close the drawer” pectin feohahie push_red_block left: “move to the red block”, “go push the red block left” rotate_red_block_right: “move to the red block”, “take the right block and rotate it to the right” eas aa push_blue_block_left: “move to the blue block”, “go push the blue block left” BAe Haw rotate_red_block_left: “move to the red block”, “take the right block and rotate it to the left” lift_pink_block slider: “move to the pink block in the slider”, “lift the pink block from the sliding cabinet” ’ A e e » iy “~ = Figure 15: Rollouts of the L-CALVIN Benchmark. Visualization of Long-VLA rollouts on the D — D split of the 10-length L-CALVIN benchmark. The figure highlights gripper camera views during the switching moments between the moving policy and interaction policy under Long-VLA, demonstrating the importance of a good initial state for completing the task.
