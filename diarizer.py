"""Basic speaker diarization for meeting transcripts."""

import re
from dataclasses import dataclass


@dataclass
class SpeakerSegment:
    speaker: str
    start: float
    end: float
    text: str


def assign_speakers_heuristic(segments: list[dict], num_speakers: int = 2) -> list[SpeakerSegment]:
    """Simple heuristic speaker assignment based on pauses and pitch changes."""
    result = []
    current_speaker = "Speaker 1"
    speaker_idx = 0

    for i, seg in enumerate(segments):
        # Switch speaker on long pauses
        if i > 0:
            gap = seg["start"] - segments[i-1]["end"]
            if gap > 1.5:
                speaker_idx = (speaker_idx + 1) % num_speakers
                current_speaker = f"Speaker {speaker_idx + 1}"

        result.append(SpeakerSegment(
            speaker=current_speaker,
            start=seg["start"],
            end=seg["end"],
            text=seg["text"],
        ))

    return result


def format_diarized_transcript(segments: list[SpeakerSegment]) -> str:
    lines = []
    for seg in segments:
        m, s = divmod(int(seg.start), 60)
        lines.append(f"[{m:02d}:{s:02d}] {seg.speaker}: {seg.text}")
    return "\n".join(lines)
