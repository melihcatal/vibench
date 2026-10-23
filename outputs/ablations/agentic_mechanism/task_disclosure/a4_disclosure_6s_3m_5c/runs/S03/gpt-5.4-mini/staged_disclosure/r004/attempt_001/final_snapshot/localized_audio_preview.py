import argparse
import base64
import os
from pathlib import Path

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_MODEL = "gpt-4o-mini-tts"


def _read_text(source: str) -> str:
    path = Path(source)
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return source


def generate_spoken_preview(text: str, output_path: str, voice: str = "alloy", speed: float = 1.0) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_TTS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODEL, "input": text, "voice": voice, "speed": speed, "response_format": "mp3"},
        timeout=120,
    )
    response.raise_for_status()

    audio_bytes = response.content
    out_path = Path(output_path)
    out_path.write_bytes(audio_bytes)
    return str(out_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate spoken previews of translated copy using OpenAI TTS.")
    parser.add_argument("input", help="Translated text or a path to a text file")
    parser.add_argument("output", help="Output MP3 file path")
    parser.add_argument("--voice", default="alloy")
    parser.add_argument("--speed", type=float, default=1.0)
    args = parser.parse_args()

    text = _read_text(args.input)
    generate_spoken_preview(text=text, output_path=args.output, voice=args.voice, speed=args.speed)


if __name__ == "__main__":
    main()
