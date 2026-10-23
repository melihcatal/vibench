import os
from typing import Optional

from openai import OpenAI


def synthesize_text(text: str, voice: str = "alloy", model: str = "gpt-4o-mini-tts") -> bytes:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    return response.read()


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit(1)
    audio = synthesize_text(sys.argv[1])
    os.write(1, audio)


if __name__ == "__main__":
    main()
