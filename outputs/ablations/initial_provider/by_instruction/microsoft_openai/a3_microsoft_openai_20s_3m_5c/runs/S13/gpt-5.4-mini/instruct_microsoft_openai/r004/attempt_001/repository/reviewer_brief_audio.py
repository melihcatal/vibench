from openai import OpenAI

from safety_client import default_audio_model, get_client
from safety_models import AudioBriefResult


def reviewer_brief_audio(text: str, voice: str = "alloy") -> AudioBriefResult:
    client: OpenAI = get_client()
    response = client.audio.speech.create(model=default_audio_model(), voice=voice, input=text)
    audio = response.read()
    return AudioBriefResult(audio_b64=audio.hex())
