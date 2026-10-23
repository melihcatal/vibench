import os
from elevenlabs import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
DEFAULT_VOICE_ID = os.environ.get("ELEVENLABS_DEFAULT_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
DEFAULT_MODEL_ID = os.environ.get(
    "ELEVENLABS_DEFAULT_MODEL_ID", "eleven_multilingual_v2"
)


def get_client():
    return ElevenLabs(api_key=ELEVENLABS_API_KEY)


def get_default_voice_id():
    return DEFAULT_VOICE_ID


def get_default_model_id():
    return DEFAULT_MODEL_ID
