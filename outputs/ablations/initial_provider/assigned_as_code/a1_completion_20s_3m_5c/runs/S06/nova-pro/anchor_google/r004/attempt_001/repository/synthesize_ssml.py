from google.cloud import texttospeech
from speech_client import get_client
from speech_models import normalize_payload, normalize_response

def synthesize_ssml(payload, config=None):
    config = config or {}
    client = get_client()
    response = client.synthesize_speech(input=texttospeech.SynthesisInput(ssml=payload["ssml"]),
        voice=texttospeech.VoiceSelectionParams(language_code=config.get("language_code", "en-US")),
        audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3))
    return normalize_response(response)