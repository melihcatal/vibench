import os

from elevenlabs.client import ElevenLabs


def reviewer_brief_audio(text):
    client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY", ""))
    audio = client.text_to_speech.convert(voice_id="21m00Tcm4TlvDq8ikWAM", model_id="eleven_multilingual_v2", text=text)
    return audio
