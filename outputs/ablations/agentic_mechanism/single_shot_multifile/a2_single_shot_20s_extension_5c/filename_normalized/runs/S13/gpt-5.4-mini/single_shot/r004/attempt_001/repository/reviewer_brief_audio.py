from typing import Any, Dict

from openai import OpenAI

from safety_client import get_openai_client


def reviewer_brief_audio(brief_text: str) -> Dict[str, Any]:
    client = get_openai_client()
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=brief_text,
        format="mp3",
    )
    return {"audio_format": "mp3", "voice": "alloy", "content_type": getattr(speech, "content_type", "audio/mpeg")}
