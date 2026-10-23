import os
from openai import OpenAI
from pathlib import Path


def platform_brief_audio(content: str, output_path: str = "platform_brief.mp3") -> str:
    """
    Generates spoken briefing audio from platform output.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set")
    client = OpenAI(api_key=api_key)
    response = client.audio.speech.create(
        input=content,
        model="tts-1-hd",
        voice="alloy",
    )
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(response.content)
    return str(path.absolute())
