"""Classify meeting type from transcript content."""

import anthropic
from config import Config

MEETING_TYPES = ["standup", "planning", "retrospective", "one_on_one", "brainstorm", "review", "general"]


class MeetingClassifier:
    SYSTEM_PROMPT = f"""Classify this meeting transcript into one of these types: {', '.join(MEETING_TYPES)}.
Return only the type name, nothing else."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def classify(self, transcript: str) -> str:
        # Use first 2000 chars for classification
        sample = transcript[:2000]

        response = self.client.messages.create(
            model=Config.MODEL,
            max_tokens=50,
            system=self.SYSTEM_PROMPT,
            messages=[{{"role": "user", "content": sample}}],
        )
        result = response.content[0].text.strip().lower()
        return result if result in MEETING_TYPES else "general"
