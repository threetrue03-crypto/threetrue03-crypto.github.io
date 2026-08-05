"""Collect recent technology links from the official Hacker News API."""

from __future__ import annotations

import concurrent.futures
import datetime as dt
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_data" / "tech_news.json"
API_ROOT = "https://hacker-news.firebaseio.com/v0"
MAX_ITEMS = 24
MAX_AGE_DAYS = 14
MIN_SCORE = 2
MAX_PER_TOPIC = 12

TOPICS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "Physical AI",
        (
            "physical ai", "embodied ai", "robot", "robotics", "humanoid",
            "autonomous vehicle", "self-driving", "isaac", "ros 2", "ros2",
        ),
    ),
    (
        "Computer Vision",
        (
            "computer vision", "vision model", "visual model", "image model",
            "object detection", "image recognition", "image segmentation",
            "semantic segmentation", "instance segmentation", "video model",
            "multimodal vision", "vision-language", "opencv",
        ),
    ),
    (
        "Computer Architecture",
        (
            "computer architecture", "cpu", "gpu", "risc-v", "risc v", "arm64",
            "semiconductor", "processor", "microarchitecture", "memory system",
            "cache coherence", "cache hierarchy", "cpu cache", "gpu cache",
            "accelerator", "cuda", "fpga", "npu", "chip design",
        ),
    ),
    (
        "Machine Learning",
        (
            "machine learning", "deep learning", "artificial intelligence", "neural network",
            "transformer", "foundation model", "language model", "llm", "inference",
            "model training", "generative ai", "reinforcement learning", "diffusion model",
            "pytorch", "tensorflow", "jax", " ai ",
        ),
    ),
)


def fetch_json(url: str, timeout: int = 12):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "sejin.dev-tech-news/1.0 (+https://threetrue03.kro.kr/)"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def classify(title: str) -> str | None:
    haystack = f" {title.lower()} "
    for topic, keywords in TOPICS:
        if any(keyword in haystack for keyword in keywords):
            return topic
    return None


def source_name(url: str) -> str:
    hostname = (urllib.parse.urlsplit(url).hostname or "Hacker News").lower()
    return hostname.removeprefix("www.")


def canonical_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
    query = [(key, value) for key, value in query if not key.lower().startswith("utm_")]
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urllib.parse.urlencode(query), "")
    )


def load_story(story_id: int) -> dict | None:
    try:
        story = fetch_json(f"{API_ROOT}/item/{story_id}.json")
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    if not story or story.get("type") != "story" or story.get("dead") or story.get("deleted"):
        return None
    if int(story.get("score", 0)) < MIN_SCORE:
        return None

    title = html.unescape(re.sub(r"\s+", " ", story.get("title", ""))).strip()
    category = classify(title)
    timestamp = int(story.get("time", 0))
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=MAX_AGE_DAYS)
    published = dt.datetime.fromtimestamp(timestamp, tz=dt.timezone.utc)
    if not title or not category or published < cutoff:
        return None

    discussion_url = f"https://news.ycombinator.com/item?id={story_id}"
    article_url = story.get("url") or discussion_url
    if not article_url.startswith(("http://", "https://")):
        return None
    article_url = canonical_url(article_url)

    return {
        "title": title,
        "url": article_url,
        "discussion_url": discussion_url,
        "source": source_name(article_url),
        "date": published.isoformat().replace("+00:00", "Z"),
        "timestamp": timestamp,
        "category": category,
        "score": int(story.get("score", 0)),
        "comments": int(story.get("descendants", 0)),
    }


def collect() -> list[dict]:
    new_ids = fetch_json(f"{API_ROOT}/newstories.json")[:300]
    top_ids = fetch_json(f"{API_ROOT}/topstories.json")[:150]
    story_ids = list(dict.fromkeys(new_ids + top_ids))

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        stories = [story for story in executor.map(load_story, story_ids) if story]

    unique: dict[str, dict] = {}
    for story in stories:
        current = unique.get(story["url"])
        if current is None or story["score"] > current["score"]:
            unique[story["url"]] = story

    ranked = sorted(
        unique.values(),
        key=lambda item: (item["timestamp"], item["score"]),
        reverse=True,
    )
    selected: list[dict] = []
    topic_counts: dict[str, int] = {}
    for story in ranked:
        category = story["category"]
        if topic_counts.get(category, 0) >= MAX_PER_TOPIC:
            continue
        selected.append(story)
        topic_counts[category] = topic_counts.get(category, 0) + 1
        if len(selected) >= MAX_ITEMS:
            break
    return [
        {
            key: value
            for key, value in story.items()
            if key not in {"score", "comments"}
        }
        for story in selected
    ]


def main() -> None:
    stories = collect()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(stories, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"기술 뉴스 {len(stories)}개를 저장했습니다: {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
