import argparse
import base64
import json
import os
import sys
from pathlib import Path

import requests


OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
OPENAI_API_URL = "https://api.openai.com/v1/audio/speech"


def _read_text(source: str | None) -> str:
    if source is None or source == "-":
        return sys.stdin.read()
    path = Path(source)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return source


def generate_audio_preview(text: str, output_path: str, voice: str = "alloy", response_format: str = "mp3") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_TTS_MODEL,
        "input": text,
        "voice": voice,
        "response_format": response_format,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(payload), timeout=120)
    response.raise_for_status()

    out = Path(output_path)
    out.write_bytes(response.content)
    return str(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate spoken previews of translated copy using OpenAI text-to-speech.")
    parser.add_argument("text", nargs="?", help="Translated copy text, a file path, or '-' for stdin")
    parser.add_argument("-o", "--output", required=True, help="Output audio file path")
    parser.add_argument("--voice", default="alloy", help="OpenAI voice name")
    parser.add_argument("--format", default="mp3", choices=["mp3", "wav", "aac", "flac", "opus"], help="Audio format")
    args = parser.parse_args()

    text = _read_text(args.text)
    if not text.strip():
        raise SystemExit("No text provided")

    result = generate_audio_preview(text=text, output_path=args.output, voice=args.voice, response_format=args.format)
    sys.stdout.write(result + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
