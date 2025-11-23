"""Draft follow-up emails from meeting notes."""

import anthropic
from config import Config


class EmailDrafter:
    SYSTEM_PROMPT = """You are a professional email writer. Given meeting notes or a transcript,
draft a concise follow-up email that:
1. Thanks participants
2. Summarizes key decisions
3. Lists action items with owners
4. Notes next steps or follow-up meeting

Keep the tone professional but friendly. The email should be ready to send with minimal editing."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def draft(self, notes: str, recipients: str | None = None) -> str:
        prompt = f"Draft a follow-up email based on these meeting notes:\n\n{notes}"
        if recipients:
            prompt += f"\n\nRecipients: {recipients}"

        response = self.client.messages.create(
            model=Config.MODEL,
            max_tokens=1024,
            system=self.SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
