import os
from typing import Optional
from openai import OpenAI

def localized_audio_preview(
    text: str,
    output_file: str,
    voice: str = "alloy",
    speed: Optional[float] = None
) -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    client = OpenAI(api_key=api_key)
    
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=text,
        speed=speed
    )
    response.stream_to_file(output_file)
