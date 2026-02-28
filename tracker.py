"""Track recurring meetings and compare notes over time."""

import json
import os
from datetime import datetime


class MeetingTracker:
    def __init__(self, data_file: str = ".meeting_tracker.json"):
        self.data_file = data_file
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.data_file):
            with open(self.data_file) as f:
                return json.load(f)
        return {"meetings": []}

    def _save(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_meeting(self, title: str, meeting_type: str, action_count: int, date: str | None = None):
        entry = {
            "title": title,
            "type": meeting_type,
            "action_items": action_count,
            "date": date or datetime.now().isoformat(),
        }
        self.data["meetings"].append(entry)
        self._save()

    def get_history(self, meeting_type: str | None = None, limit: int = 10) -> list[dict]:
        meetings = self.data["meetings"]
        if meeting_type:
            meetings = [m for m in meetings if m["type"] == meeting_type]
        return meetings[-limit:]
