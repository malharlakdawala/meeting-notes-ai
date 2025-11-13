"""Extract action items from meeting transcripts."""

import anthropic
import json
import re
from config import Config
from pydantic import BaseModel
from typing import Optional


class ActionItem(BaseModel):
    description: str
    owner: Optional[str] = None
    deadline: Optional[str] = None
    priority: str = "medium"


class ActionExtractor:
    SYSTEM_PROMPT = """Extract action items from this meeting transcript. Return a JSON array where each item has:
- description: what needs to be done
- owner: who is responsible (null if not mentioned)
- deadline: when it's due (null if not mentioned)
- priority: "high", "medium", or "low"

Return ONLY the JSON array, no other text."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def extract(self, transcript: str) -> list[ActionItem]:
        response = self.client.messages.create(
            model=Config.MODEL,
            max_tokens=1024,
            system=self.SYSTEM_PROMPT,
            messages=[{"role": "user", "content": transcript}],
        )
        text = response.content[0].text

        try:
            # Handle markdown code blocks
            json_match = re.search(r"```(?:json)?\s*(.+?)```", text, re.DOTALL)
            raw = json_match.group(1) if json_match else text

            items = json.loads(raw)
            return [ActionItem(**item) for item in items]
        except (json.JSONDecodeError, KeyError) as e:
            return []

    def format_markdown(self, items: list[ActionItem]) -> str:
        if not items:
            return "No action items found."

        lines = ["## Action Items\n"]
        for item in items:
            checkbox = "- [ ]"
            owner = f" (@{item.owner})" if item.owner else ""
            deadline = f" - due: {item.deadline}" if item.deadline else ""
            priority_icon = {"high": "!!!", "medium": "", "low": ""}.get(item.priority, "")
            lines.append(f"{checkbox} {priority_icon} {item.description}{owner}{deadline}")

        return "\n".join(lines)
