---
layout: post
type: note
title: "Transcoding & Remuxing"
description: "컨테이너와 코덱의 호환성을 해결하기 위한 두 가지 방법을 소개한다."
date: 2026-06-25
category: FFmpeg
tags: [FFmpeg, Transcoding, Remuxing, Video]
---

# Transcoding & Remuxing

> 컨테이너 안의 코덱 조합이 불안정할 수 있다.
> 이럴 때는, 프로그래머가 트랜스코딩 또는 리먹싱을 이용하여 해결해야 한다.

## Transcoding이란?
트랜스코딩은 코덱 자체를 바꾸기 위해 다시 압축하는 과정이다.

```
기존 코덱으로 압축 해제
↓
새 코덱으로 다시 압축
```

트랜스코딩을 하는 법은 다음과 같다.

```bash
ffmpeg -i "input.avi" -c:v libx264 -c:a aac "output.mp4"
```

`-i "input.avi"`는 입력 파일로 input.avi를 사용한다는 것이다.
`-c:v libx264`에서 c는 codec의 줄임이고 v는 video의 줄임이다. H.264로 input.avi를 압축하라는 뜻이다.
`-c:a aac`에서 a는 audio이다. AAC 코덱으로 다시 압축하라는 뜻이다.

```
input.avi 읽기
↓
기존 비디오 코덱으로 압축 해제
↓
H.264로 다시 압축
↓
오디오는 AAC로 다시 압축
↓
MP4 파일로 저장
```

트랜스코딩을 하게 되면 압축 데이터를 건들기 때문에 화질이 손상될 수 있는 가능성이 있다.

## Remuxing이란?
리먹싱은 압축 데이터는 그대로 두고 컨테이너만 바꾸는 과정이다.

```bash
ffmpeg -i "input.avi" -c copy "output.mp4"
```

여기서 `-c copy`는 비디오/오디오 압축 데이터를 그대로 복사하고 컨테이너만 바꾸라는 뜻이다.

**주의!! 단순히 windows에서 제공하는 이름 바꾸기로 avi확장명을 mp4로 바꾼다고 해서 컨테이너는 바뀌지 않는다.**
원래 파일이 다음과 같다고 하자.

```
input.avi
├─ 컨테이너: AVI
├─ 비디오 코덱: Xvid
└─ 오디오 코덱: MP3
```

이름만 바꾸게 되면

```
input.mp4
├─ 실제 컨테이너: AVI
├─ 비디오 코덱: Xvid
└─ 오디오 코덱: MP3
```

즉, 겉 이름은 .mp4가 되었지만 파일 내부는 여전히 .avi이다.
그래서 리먹싱을 하는 것이다.
