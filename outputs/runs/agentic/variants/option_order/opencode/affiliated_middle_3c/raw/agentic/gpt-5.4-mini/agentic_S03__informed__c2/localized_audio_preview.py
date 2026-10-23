import os

from elevenlabs import generate, set_api_key


def localized_audio_preview(text: str):
    set_api_key(os.environ.get("ELEVENLABS_API_KEY", ""))
    return generate(text=text, voice="Rachel", model="eleven_multilingual_v2")
