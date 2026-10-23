import os
from elevenlabs import ElevenLabs


def get_elevenlabs_client(api_key=None):
    api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable is required")
    return ElevenLabs(api_key=api_key)


def get_default_voice_id():
    return os.environ.get("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")


def get_default_model_id():
    return os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")


def get_default_output_format():
    return os.environ.get("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128")
