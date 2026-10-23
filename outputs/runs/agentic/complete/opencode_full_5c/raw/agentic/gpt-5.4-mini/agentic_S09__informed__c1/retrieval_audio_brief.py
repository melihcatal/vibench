import os

from elevenlabs.client import ElevenLabs


def generate_spoken_brief(results):
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")
    client = ElevenLabs(api_key=api_key)
    text = " ".join(str(item) for item in results)
    audio = client.text_to_speech.convert(
        text=text, voice_id="Rachel", model_id="eleven_multilingual_v2"
    )
    return audio
