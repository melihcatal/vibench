import os
from typing import Any, Dict, Iterable, Optional

import openai


def generate_spoken_briefing(
    platform_output: str,
    locale: str = "en",
    voice: str = "alloy",
    model: str = "gpt-4o-mini-tts",
    instructions: Optional[str] = None,
) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    text = platform_output.strip()
    prompt = instructions or f"Create a concise spoken briefing in {locale} based on the provided platform output."
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=f"{prompt}\n\n{text}",
        response_format="mp3",
    )
    audio_bytes = b""
    if hasattr(response, "read"):
        audio_bytes = response.read()
    elif hasattr(response, "content"):
        audio_bytes = response.content
    return {
        "provider": "openai",
        "model": model,
        "voice": voice,
        "locale": locale,
        "audio": audio_bytes,
    }
