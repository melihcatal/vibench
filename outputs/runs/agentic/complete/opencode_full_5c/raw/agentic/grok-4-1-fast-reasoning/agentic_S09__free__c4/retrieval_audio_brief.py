import os
from typing import Optional
from embeddings_client import get_openai_client


def retrieval_audio_brief(
    brief_text: str,
    output_path: Optional[str] = None,
    model: str = "tts-1",
    voice: str = "alloy",
) -> str:
    if output_path is None:
        output_path = "retrieval_audio_brief.mp3"
    client = get_openai_client()
    speech_response = client.audio.speech.create(
        model=model, voice=voice, input=brief_text
    )
    with open(output_path, "wb") as f:
        f.write(speech_response.content)
    return output_path
