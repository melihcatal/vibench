import os
import sys
from pathlib import Path

from openai import OpenAI


def transcribe_audio(audio_path: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    path = Path(audio_path)
    with path.open("rb") as audio_file:
        result = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return result.text


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python tts_qa_transcript.py <audio_file>")
    transcript = transcribe_audio(sys.argv[1])
    sys.stdout.write(transcript)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
