import os
from typing import Optional, Union

from openai import OpenAI


def synthesize_ssml(
    ssml: str,
    voice: str = "alloy",
    speed: float = 1.0,
    model: str = "gpt-4o-mini-tts",
    output_path: Optional[str] = None,
) -> Union[bytes, str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=ssml,
        response_format="mp3",
        speed=speed,
    )
    audio = response.read()
    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio)
        return output_path
    return audio
