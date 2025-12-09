"""Process multiple meeting recordings in batch."""

import os
import logging
from pathlib import Path
from rich.progress import Progress

from transcriber import Transcriber
from summarizer import MeetingSummarizer
from action_items import ActionExtractor
from config import Config

logger = logging.getLogger(__name__)


def process_directory(input_dir: str, output_dir: str | None = None):
    output_dir = output_dir or Config.OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    audio_extensions = {".mp3", ".mp4", ".wav", ".m4a", ".webm"}
    files = [f for f in Path(input_dir).iterdir() if f.suffix.lower() in audio_extensions]

    if not files:
        logger.warning(f"No audio files found in {input_dir}")
        return

    transcriber = Transcriber()
    summarizer = MeetingSummarizer()
    extractor = ActionExtractor()

    with Progress() as progress:
        task = progress.add_task("Processing meetings...", total=len(files))

        for audio_file in sorted(files):
            base = audio_file.stem
            logger.info(f"Processing: {audio_file.name}")

            try:
                result = transcriber.transcribe(str(audio_file))
                transcript_path = os.path.join(output_dir, f"{base}_transcript.txt")
                transcriber.save_transcript(result, transcript_path)

                notes = summarizer.summarize(result["text"])
                with open(os.path.join(output_dir, f"{base}_notes.md"), "w") as f:
                    f.write(notes)

                items = extractor.extract(result["text"])
                with open(os.path.join(output_dir, f"{base}_actions.md"), "w") as f:
                    f.write(extractor.format_markdown(items))

            except Exception as e:
                logger.error(f"Failed to process {audio_file.name}: {e}")

            progress.advance(task)
