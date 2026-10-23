import base64
import os
from pathlib import Path
from typing import Optional

import requests


OPENAI_TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def generate_spoken_preview(
    translated_copy: str,
    output_path: str,
    *,
    voice: str = "alloy",
    format: str = "mp3",
    model: str = OPENAI_TTS_MODEL,
    api_key: Optional[str] = None,
) -> str:
    if not translated_copy or not translated_copy.strip():
        raise ValueError("translated_copy must not be empty")

    token = api_key or os.environ.get("OPENAI_API_KEY")
    if not token:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": model,
        "input": translated_copy,
        "voice": voice,
        "response_format": format,
    }
    response = requests.post(
        OPENAI_TTS_ENDPOINT,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    response.raise_for_status()

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        data = response.json()
        audio_b64 = data.get("audio") or data.get("data")
        if not audio_b64:
            raise RuntimeError("OpenAI response did not contain audio data")
        out.write_bytes(base64.b64decode(audio_b64))
    else:
        out.write_bytes(response.content)

    return str(out)


def generate_spoken_preview_from_file(input_path: str, output_path: str, **kwargs) -> str:
    translated_copy = Path(input_path).read_text(encoding="utf-8")
    return generate_spoken_preview(translated_copy, output_path, **kwargs)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate spoken previews of translated copy using OpenAI TTS")
    parser.add_argument("input", help="Path to a text file containing translated copy")
    parser.add_argument("output", help="Path to write the generated audio preview")
    parser.add_argument("--voice", default="alloy")
    parser.add_argument("--format", default="mp3")
    parser.add_argument("--model", default=OPENAI_TTS_MODEL)
    args = parser.parse_args()

    generate_spoken_preview_from_file(
        args.input,
        args.output,
        voice=args.voice,
        format=args.format,
        model=args.model,
    )
