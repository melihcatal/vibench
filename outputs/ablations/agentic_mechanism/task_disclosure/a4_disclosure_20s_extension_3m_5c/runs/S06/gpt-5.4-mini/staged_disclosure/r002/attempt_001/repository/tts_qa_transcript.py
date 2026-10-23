import base64
import json
import os
import sys
from pathlib import Path

import requests


OPENAI_TRANSCRIBE_URL = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_TRANSCRIBE_MODEL = "gpt-4o-mini-transcribe"


def transcribe_audio_file(audio_path: Path) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    with audio_path.open("rb") as audio_file:
        response = requests.post(
            OPENAI_TRANSCRIBE_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (audio_path.name, audio_file)},
            data={"model": OPENAI_TRANSCRIBE_MODEL},
            timeout=120,
        )

    response.raise_for_status()
    payload = response.json()
    return payload.get("text", "")


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("usage: tts_qa_transcript.py <audio-file>")

    audio_path = Path(sys.argv[1])
    transcript = transcribe_audio_file(audio_path)
    print(json.dumps({"file": str(audio_path), "transcript": transcript}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
