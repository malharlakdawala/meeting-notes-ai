"""CLI for meeting-notes-ai."""

import os
import click
from rich.console import Console
from rich.markdown import Markdown

from config import Config
from transcriber import Transcriber
from summarizer import MeetingSummarizer
from action_items import ActionExtractor
from email_drafter import EmailDrafter

console = Console()


@click.group()
def cli():
    """Meeting Notes AI - Transcribe and summarize meetings."""
    pass


@cli.command()
@click.argument("audio_file")
@click.option("--output", "-o", default=None, help="Output transcript file")
def transcribe(audio_file: str, output: str | None):
    """Transcribe an audio file."""
    transcriber = Transcriber()
    result = transcriber.transcribe(audio_file)

    output = output or os.path.join(Config.OUTPUT_DIR, "transcript.txt")
    transcriber.save_transcript(result, output)
    console.print(f"[green]Transcript saved to {output}[/green]")
    console.print(f"Duration: {result['duration']:.0f}s, Language: {result['language']}")


@cli.command()
@click.argument("transcript_file")
@click.option("--output", "-o", default=None, help="Output notes file")
def notes(transcript_file: str, output: str | None):
    """Generate meeting notes from a transcript."""
    with open(transcript_file) as f:
        transcript = f.read()

    summarizer = MeetingSummarizer()
    result = summarizer.summarize(transcript)

    if output:
        with open(output, "w") as f:
            f.write(result)
        console.print(f"[green]Notes saved to {output}[/green]")
    else:
        console.print(Markdown(result))


@cli.command()
@click.argument("transcript_file")
def actions(transcript_file: str):
    """Extract action items from a transcript."""
    with open(transcript_file) as f:
        transcript = f.read()

    extractor = ActionExtractor()
    items = extractor.extract(transcript)
    md = extractor.format_markdown(items)
    console.print(Markdown(md))


@cli.command()
@click.argument("transcript_file")
@click.option("--to", "recipients", default=None, help="Email recipients")
def followup(transcript_file: str, recipients: str | None):
    """Draft a follow-up email."""
    with open(transcript_file) as f:
        transcript = f.read()

    drafter = EmailDrafter()
    email = drafter.draft(transcript, recipients)
    console.print(email)


@cli.command()
@click.argument("audio_file")
def process(audio_file: str):
    """Full pipeline: transcribe -> notes -> actions."""
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(audio_file))[0]

    # Transcribe
    console.print("[bold]Step 1: Transcribing...[/bold]")
    transcriber = Transcriber()
    result = transcriber.transcribe(audio_file)
    transcript_path = os.path.join(Config.OUTPUT_DIR, f"{base_name}_transcript.txt")
    transcriber.save_transcript(result, transcript_path)
    console.print(f"  Transcript saved: {transcript_path}")

    # Generate notes
    console.print("[bold]Step 2: Generating notes...[/bold]")
    summarizer = MeetingSummarizer()
    notes_text = summarizer.summarize(result["text"])
    notes_path = os.path.join(Config.OUTPUT_DIR, f"{base_name}_notes.md")
    with open(notes_path, "w") as f:
        f.write(notes_text)
    console.print(f"  Notes saved: {notes_path}")

    # Extract actions
    console.print("[bold]Step 3: Extracting action items...[/bold]")
    extractor = ActionExtractor()
    items = extractor.extract(result["text"])
    actions_md = extractor.format_markdown(items)
    actions_path = os.path.join(Config.OUTPUT_DIR, f"{base_name}_actions.md")
    with open(actions_path, "w") as f:
        f.write(actions_md)
    console.print(f"  Actions saved: {actions_path}")

    console.print(f"\n[green]Done! All output in {Config.OUTPUT_DIR}/[/green]")


if __name__ == "__main__":
    cli()
