from __future__ import annotations

import os
from typing import Optional

from model_client import create_speech
from model_models import SpeechRequest, SpeechResponse


def generate_spoken_brief(
    text: str,
    voice: str = "alloy",
    model: str = "tts-1",
    speed: float = 1.0,
    response_format: str = "mp3",
) -> SpeechResponse:
    request = SpeechRequest(
        input_text=text,
        model=model,
        voice=voice,
        speed=speed,
        response_format=response_format,
    )
    return create_speech(request)


def save_spoken_brief(
    text: str,
    output_path: str,
    voice: str = "alloy",
    model: str = "tts-1",
    speed: float = 1.0,
    response_format: str = "mp3",
) -> str:
    response = generate_spoken_brief(
        text=text,
        voice=voice,
        model=model,
        speed=speed,
        response_format=response_format,
    )
    with open(output_path, "wb") as f:
        f.write(response.audio_bytes)
    return output_path


def generate_brief_from_summary(
    summary_text: str,
    voice: str = "alloy",
    model: str = "tts-1",
    speed: float = 1.0,
) -> SpeechResponse:
    brief_intro = "Here is a brief summary. "
    formatted_text = brief_intro + summary_text
    return generate_spoken_brief(
        text=formatted_text,
        voice=voice,
        model=model,
        speed=speed,
    )


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read()
    output_file = os.environ.get("SPOKEN_BRIEF_OUTPUT", "output.mp3")
    result = save_spoken_brief(input_text, output_file)
    print(f"Audio saved to: {result}")
