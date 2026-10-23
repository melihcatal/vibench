import os
from elevenlabs import ElevenLabs


ELEVENLABS_API_KEY_ENV = "ELEVENLABS_API_KEY"
ELEVENLABS_DEFAULT_VOICE = "EXAVITQu4vr4xnSDxMaL"
ELEVENLABS_DEFAULT_MODEL = "eleven_multilingual_v2"


def get_elevenlabs_api_key() -> str:
    api_key = os.environ.get(ELEVENLABS_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"ElevenLabs API key not found. Set the {ELEVENLABS_API_KEY_ENV} environment variable."
        )
    return api_key


def get_elevenlabs_client(api_key: str = None) -> ElevenLabs:
    if api_key is None:
        api_key = get_elevenlabs_api_key()
    return ElevenLabs(api_key=api_key)


def get_default_voice_id() -> str:
    return os.environ.get("ELEVENLABS_VOICE_ID", ELEVENLABS_DEFAULT_VOICE)


def get_default_model_id() -> str:
    return os.environ.get("ELEVENLABS_MODEL_ID", ELEVENLABS_DEFAULT_MODEL)
