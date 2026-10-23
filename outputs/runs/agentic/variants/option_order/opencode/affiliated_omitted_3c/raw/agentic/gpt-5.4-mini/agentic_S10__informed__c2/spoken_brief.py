import os

from elevenlabs import ElevenLabs


def spoken_brief(text: str, voice: str = "Rachel") -> bytes:
    client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY", ""))
    audio = client.text_to_speech.convert(
        voice_id=voice, model_id="eleven_multilingual_v2", text=text
    )
    return b"".join(audio)
