from __future__ import annotations

from openai import OpenAI


OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
OPENAI_TTS_VOICE = "alloy"



def platform_brief_audio(text: str, instructions: str = "Speak in a concise executive briefing tone.") -> dict:
    client = OpenAI()
    response = client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=OPENAI_TTS_VOICE,
        input=text,
        instructions=instructions,
        format="mp3",
    )
    audio_bytes = response.read()
    return {
        "model": OPENAI_TTS_MODEL,
        "voice": OPENAI_TTS_VOICE,
        "audio_bytes": audio_bytes,
        "content_type": "audio/mpeg",
    }
