# meeting-notes-ai

Transcribe meeting recordings with Whisper and generate structured notes, action items, and follow-up emails using Claude.

## Features

- **Transcription** - Local Whisper transcription (no data leaves your machine)
- **Smart Notes** - AI-generated structured meeting notes
- **Action Items** - Automatic extraction with owners and deadlines
- **Follow-up Emails** - Draft follow-up emails for meeting participants
- **Export** - Markdown and Notion export options

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
# Full pipeline: transcribe + generate notes
python cli.py process recording.mp3

# Transcribe only
python cli.py transcribe recording.mp3

# Generate notes from existing transcript
python cli.py notes transcript.txt

# Extract action items
python cli.py actions transcript.txt

# Draft follow-up email
python cli.py followup transcript.txt --to "team@company.com"
```
