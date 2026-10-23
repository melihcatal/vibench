from google.cloud import texttospeech

from speech_client import client, load_config
from speech_models import audio_config_from_config, normalize_ssml_payload, voice_params_from_config


def synthesize_ssml(payload, config=None):
    config = load_config(config)
    payload = normalize_ssml_payload(payload)
    response = client().synthesize_speech(
        input=texttospeech.SynthesisInput(ssml=payload["ssml"]),
        voice=voice_params_from_config(config),
        audio_config=audio_config_from_config(config),
    )
    return {"audio_bytes": response.audio_content, "content_type": "audio/mpeg"}
