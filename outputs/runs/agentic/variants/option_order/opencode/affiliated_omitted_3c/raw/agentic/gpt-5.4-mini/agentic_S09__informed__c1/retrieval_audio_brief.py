import os

from elevenlabs.client import ElevenLabs


def retrieval_audio_brief(summary: str) -> bytes:
    client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))
    audio = client.text_to_speech.convert(
        text=summary, voice_id="21m00Tcm4TlvDq8ikWAM", model_id="eleven_multilingual_v2"
    )
    return b"".join(audio)
