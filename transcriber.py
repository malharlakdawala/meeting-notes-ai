"""Audio transcription using OpenAI Whisper."""

import whisper
import logging
import os
from pathlib import Path
from config import Config

logger = logging.getLogger(__name__)


class Transcriber:
    SUPPORTED_FORMATS = {".mp3", ".mp4", ".wav", ".m4a", ".webm", ".ogg"}

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or Config.WHISPER_MODEL
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Loading Whisper model: {self.model_name}")
            self._model = whisper.load_model(self.model_name)
        return self._model

    def transcribe(self, audio_path: str) -> dict:
        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported audio format: {path.suffix}")

        logger.info(f"Transcribing: {audio_path}")
        result = self.model.transcribe(str(path), verbose=False)

        return {
            "text": result["text"],
            "segments": [
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"].strip(),
                }
                for seg in result["segments"]
            ],
            "language": result.get("language", "en"),
            "duration": result["segments"][-1]["end"] if result["segments"] else 0,
        }

    def save_transcript(self, result: dict, output_path: str):
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w") as f:
            for seg in result["segments"]:
                start = self._format_time(seg["start"])
                end = self._format_time(seg["end"])
                f.write(f"[{start} - {end}] {seg['text']}\n")

    @staticmethod
    def _format_time(seconds: float) -> str:
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
