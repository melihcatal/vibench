import os
import sys
from pathlib import Path

from openai import OpenAI


def transcribe_audio(audio_path: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
    return result.text


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: tts_qa_transcript.py <audio-file>")
        return 2

    audio_path = Path(sys.argv[1])
    if not audio_path.is_file():
        print(f"file not found: {audio_path}")
        return 1

    print(transcribe_audio(str(audio_path)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
