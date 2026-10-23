import json
import os
import sys
from pathlib import Path

import requests


OPENAI_TRANSCRIBE_URL = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_MODEL = "whisper-1"


def transcribe_audio(audio_path: Path) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    with audio_path.open("rb") as audio_file:
        response = requests.post(
            OPENAI_TRANSCRIBE_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (audio_path.name, audio_file, "application/octet-stream")},
            data={"model": OPENAI_MODEL},
            timeout=120,
        )
    response.raise_for_status()
    payload = response.json()
    return payload.get("text", "")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python tts_qa_transcript.py <audio-file>")
    audio_path = Path(sys.argv[1])
    if not audio_path.is_file():
        raise FileNotFoundError(str(audio_path))
    transcript = transcribe_audio(audio_path)
    print(json.dumps({"file": str(audio_path), "transcript": transcript}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
