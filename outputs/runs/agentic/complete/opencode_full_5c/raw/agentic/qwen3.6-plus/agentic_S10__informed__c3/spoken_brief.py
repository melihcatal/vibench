import os
from typing import Optional
from elevenlabs import ElevenLabs
from model_models import SpeechResult


def generate_spoken_brief(
    text: str,
    voice: str = "Rachel",
    model: str = "eleven_multilingual_v2",
    api_key: Optional[str] = None,
) -> SpeechResult:
    key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    client = ElevenLabs(api_key=key)

    audio_generator = client.generate(
        text=text,
        voice=voice,
        model=model,
    )

    audio_data = b"".join(audio_generator)

    return SpeechResult(
        audio_data=audio_data,
        format="mp3",
    )
