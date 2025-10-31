"""Claude-based meeting summary generation."""

import anthropic
from config import Config


class MeetingSummarizer:
    SYSTEM_PROMPT = """You are a meeting notes assistant. Given a meeting transcript, generate structured notes with:

1. **Meeting Summary** - 2-3 sentence overview
2. **Key Discussion Points** - Main topics discussed (bullet points)
3. **Decisions Made** - Any decisions or agreements reached
4. **Action Items** - Tasks assigned with owners (if mentioned) and deadlines (if mentioned)
5. **Open Questions** - Unresolved items that need follow-up

Use markdown formatting. Be concise but comprehensive. Extract actual names when mentioned."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def summarize(self, transcript: str) -> str:
        response = self.client.messages.create(
            model=Config.MODEL,
            max_tokens=2048,
            system=self.SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Generate meeting notes from this transcript:\n\n{transcript}",
            }],
        )
        return response.content[0].text
