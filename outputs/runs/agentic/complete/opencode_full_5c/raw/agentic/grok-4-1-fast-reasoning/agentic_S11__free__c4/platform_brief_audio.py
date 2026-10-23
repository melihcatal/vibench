import os
import openai
from pathlib import Path


def platform_brief_audio(
    text: str, voice: str = "alloy", output_path: str = "briefing.mp3"
) -> None:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
