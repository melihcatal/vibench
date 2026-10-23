from __future__ import annotations

from openai import OpenAI

from model_client import DEFAULT_TTS_MODEL, DEFAULT_TTS_VOICE, HostedModelClient
from model_models import AudioSpeechResult


def spoken_brief(text: str, voice: str = DEFAULT_TTS_VOICE) -> AudioSpeechResult:
    inference_client = HostedModelClient()
    brief_request = inference_client.build_request(
        task="summarization",
        system_prompt="Create a brief spoken-ready summary in 3 to 5 sentences with natural pacing.",
        user_prompt=f"Prepare a spoken brief for this content:\n\n{text}",
        temperature=0.3,
        max_tokens=180,
    )
    brief = inference_client.generate(brief_request)

    audio_client = OpenAI()
    speech = audio_client.audio.speech.create(
        model=DEFAULT_TTS_MODEL,
        voice=voice,
        input=brief.text,
    )
    return AudioSpeechResult(
        audio_bytes=speech.read(),
        model=DEFAULT_TTS_MODEL,
        voice=voice,
    )
