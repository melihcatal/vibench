from __future__ import annotations

import base64

from model_client import DEFAULT_TTS_MODEL, get_openai_client, messages_to_dicts
from model_models import TextGenerationResult, normalize_messages, usage_to_dict


def generate_spoken_brief(source_text: str, voice: str = "alloy") -> dict:
    client = get_openai_client()
    brief_messages = normalize_messages(
        system_prompt="Create a short spoken brief optimized for audio delivery.",
        user_prompt=f"Write a spoken brief based on this content:\n\n{source_text}",
    )
    brief_response = client.responses.create(
        model="gpt-4.1-mini",
        input=messages_to_dicts(brief_messages),
        temperature=0.4,
        max_output_tokens=250,
    )
    transcript = brief_response.output_text
    audio_response = client.audio.speech.create(
        model=DEFAULT_TTS_MODEL,
        voice=voice,
        input=transcript,
        format="mp3",
    )
    audio_bytes = audio_response.read()
    text_result = TextGenerationResult(
        provider="openai",
        model="gpt-4.1-mini",
        text=transcript,
        usage=usage_to_dict(
            input_tokens=getattr(brief_response.usage, "input_tokens", None)
            if getattr(brief_response, "usage", None)
            else None,
            output_tokens=getattr(brief_response.usage, "output_tokens", None)
            if getattr(brief_response, "usage", None)
            else None,
            total_tokens=getattr(brief_response.usage, "total_tokens", None)
            if getattr(brief_response, "usage", None)
            else None,
        ),
    )
    return {
        "provider": "openai",
        "tts_model": DEFAULT_TTS_MODEL,
        "voice": voice,
        "brief": text_result.text,
        "audio_base64": base64.b64encode(audio_bytes).decode("utf-8"),
        "usage": text_result.usage,
    }
