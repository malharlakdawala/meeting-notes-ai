"""Export meeting notes to Notion."""

import requests
import logging
import os

logger = logging.getLogger(__name__)

NOTION_API = "https://api.notion.com/v1"


class NotionExporter:
    def __init__(self):
        self.token = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_DATABASE_ID")

    def export(self, title: str, content: str, date: str | None = None) -> str | None:
        if not self.token or not self.database_id:
            logger.warning("Notion credentials not configured")
            return None

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

        # Create page in database
        page_data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": title}}]},
            },
            "children": self._markdown_to_blocks(content),
        }

        if date:
            page_data["properties"]["Date"] = {"date": {"start": date}}

        try:
            response = requests.post(
                f"{NOTION_API}/pages",
                json=page_data,
                headers=headers,
                timeout=15,
            )
            response.raise_for_status()
            page_id = response.json()["id"]
            logger.info(f"Created Notion page: {page_id}")
            return page_id
        except requests.RequestException as e:
            logger.error(f"Notion export failed: {e}")
            return None

    def _markdown_to_blocks(self, content: str) -> list[dict]:
        blocks = []
        for line in content.split("\n"):
            if line.startswith("# "):
                blocks.append({"object": "block", "type": "heading_1",
                    "heading_1": {"rich_text": [{"text": {"content": line[2:]}}]}})
            elif line.startswith("## "):
                blocks.append({"object": "block", "type": "heading_2",
                    "heading_2": {"rich_text": [{"text": {"content": line[3:]}}]}})
            elif line.startswith("- "):
                blocks.append({"object": "block", "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": [{"text": {"content": line[2:]}}]}})
            elif line.strip():
                blocks.append({"object": "block", "type": "paragraph",
                    "paragraph": {"rich_text": [{"text": {"content": line}}]}})
        return blocks[:100]  # Notion API limit
