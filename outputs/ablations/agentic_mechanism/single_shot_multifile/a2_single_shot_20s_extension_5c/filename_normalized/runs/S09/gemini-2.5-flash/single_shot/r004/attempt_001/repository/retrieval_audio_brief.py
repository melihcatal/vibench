import os
import openai
from typing import Union

def generate_audio_brief(text: str, output_path: Union[str, None] = None) -> bytes:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    audio_bytes = response.content
    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
    return audio_bytes
