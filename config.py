"""Configuration."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
    MODEL = os.getenv("MODEL", "claude-sonnet-4-20250514")
