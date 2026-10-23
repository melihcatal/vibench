import boto3

from speech_client import load_config
from speech_models import normalize_ssml_payload


def synthesize_ssml(payload, config=None):
    cfg = load_config(config)
    data = normalize_ssml_payload(payload)
    client = boto3.client("polly", region_name=cfg.region)
    response = client.synthesize_speech(
        Text=data["ssml"],
        TextType="ssml",
        OutputFormat=data.get("output_format", cfg.output_format),
        VoiceId=data.get("voice_id", cfg.voice_id),
        Engine=data.get("engine", "neural"),
    )
    stream = response["AudioStream"]
    try:
        return {"audio_bytes": stream.read(), "content_type": "audio/mpeg"}
    finally:
        stream.close()
