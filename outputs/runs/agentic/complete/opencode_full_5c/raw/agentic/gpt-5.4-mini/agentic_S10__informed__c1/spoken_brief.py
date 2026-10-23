import os

from elevenlabs import ElevenLabs


def generate_spoken_brief(text: str, voice_id: str | None = None) -> bytes:
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio = client.text_to_speech.convert(
        voice_id=voice_id or os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM"),
        model_id="eleven_multilingual_v2",
        text=text,
    )
    return b"".join(audio)
