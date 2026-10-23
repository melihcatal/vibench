import boto3

from speech_client import get_speech_client
from speech_models import normalize_ssml_payload


def synthesize_ssml(payload, config=None):
    config = config or {}
    client = get_speech_client(config)
    normalized_payload = normalize_ssml_payload(payload)
    response = client.synthesize_speech(Text=normalized_payload["text"], TextType="ssml", OutputFormat="mp3",
                                       VoiceId=config.get("voice_id", "Joanna"))
    stream = response["AudioStream"]
    try:
        return {"audio_bytes": stream.read(), "content_type": "audio/mpeg"}
    finally:
        stream.close()