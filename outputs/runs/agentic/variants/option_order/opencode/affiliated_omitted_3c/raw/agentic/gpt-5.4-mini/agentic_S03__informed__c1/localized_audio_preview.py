import os

from elevenlabs.client import ElevenLabs


def localized_audio_preview(text: str):
    client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])
    return client.text_to_speech.convert(text=text, voice_id="Rachel", model_id="eleven_multilingual_v2")
