import os
from elevenlabs import generate, set_api_key
from model_models import ModelResponse, AudioResult


def generate_audio_briefing(response: ModelResponse) -> AudioResult:
    """
    Generates an audio briefing from text using ElevenLabs.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    set_api_key(api_key)

    audio = generate(text=response.text, voice="Rachel", model="eleven_multilingual_v2")

    return AudioResult(audio_content=audio)
