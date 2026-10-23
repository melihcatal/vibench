from google.cloud import texttospeech

from speech_client import audio_encoding, get_client, normalize_language_code
from speech_models import normalize_config, normalize_payload


def synthesize_ssml(payload, config=None):
    payload = normalize_payload(payload)
    config = normalize_config(config)
    client = get_client()
    response = client.synthesize_speech(input=texttospeech.SynthesisInput(ssml=payload["ssml"]), voice=texttospeech.VoiceSelectionParams(language_code=normalize_language_code(config.get("language_code")), name=config.get("voice_name")), audio_config=texttospeech.AudioConfig(audio_encoding=audio_encoding(config.get("audio_encoding", "MP3")), speaking_rate=config.get("speaking_rate", 1.0), pitch=config.get("pitch", 0.0)))
    return {"audio_bytes": response.audio_content, "content_type": "audio/mpeg"}
