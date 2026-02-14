"""Meeting metadata analysis."""

import re
from dataclasses import dataclass


@dataclass
class MeetingMetadata:
    estimated_duration_minutes: int
    participant_count: int
    participants: list[str]
    language: str
    topic_keywords: list[str]


def analyze_transcript(text: str, segments: list[dict] | None = None) -> MeetingMetadata:
    # Estimate duration from segments
    duration = 0
    if segments and len(segments) > 0:
        duration = int(segments[-1].get("end", 0) / 60)

    # Detect participants from common patterns
    name_pattern = re.compile(r"(?:^|\n)([A-Z][a-z]+ [A-Z][a-z]+):", re.MULTILINE)
    speaker_pattern = re.compile(r"Speaker (\d+)")
    names = list(set(name_pattern.findall(text)))
    speakers = list(set(speaker_pattern.findall(text)))

    participants = names if names else [f"Speaker {s}" for s in speakers]
    participant_count = len(participants) if participants else 2

    # Extract topic keywords (simple frequency-based)
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    stopwords = {"this", "that", "with", "from", "they", "have", "been", "were", "will", "would", "could", "should", "about", "their", "there", "when", "what", "which", "more", "some", "also", "just", "than"}
    word_freq = {}
    for w in words:
        if w not in stopwords:
            word_freq[w] = word_freq.get(w, 0) + 1
    keywords = sorted(word_freq, key=word_freq.get, reverse=True)[:10]

    return MeetingMetadata(
        estimated_duration_minutes=duration,
        participant_count=participant_count,
        participants=participants,
        language="en",
        topic_keywords=keywords,
    )
