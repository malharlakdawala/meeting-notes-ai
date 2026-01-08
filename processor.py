"""Transcript processing and cleaning."""

import re


FILLER_WORDS = [
    r"\b(um|uh|uhm|hmm|huh|ah|oh|er|erm)\b",
    r"\b(you know|like|basically|actually|literally|right)\b(?=,|\s)",
    r"\b(sort of|kind of|i mean|i guess)\b",
]

FILLER_PATTERN = re.compile("|".join(FILLER_WORDS), re.IGNORECASE)


def clean_transcript(text: str, remove_fillers: bool = True) -> str:
    if remove_fillers:
        text = FILLER_PATTERN.sub("", text)

    # Collapse multiple spaces
    text = re.sub(r"\s{2,}", " ", text)
    # Fix punctuation spacing
    text = re.sub(r"\s+([,.])", r"\1", text)
    # Capitalize after periods
    text = re.sub(r"\.\s+(\w)", lambda m: ". " + m.group(1).upper(), text)

    return text.strip()


def split_into_segments(text: str, max_length: int = 4000) -> list[str]:
    """Split long transcript into processable segments."""
    if len(text) <= max_length:
        return [text]

    segments = []
    sentences = re.split(r"(?<=[.!?])\s+", text)
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) > max_length and current:
            segments.append(current.strip())
            current = sentence
        else:
            current += " " + sentence

    if current.strip():
        segments.append(current.strip())

    return segments
