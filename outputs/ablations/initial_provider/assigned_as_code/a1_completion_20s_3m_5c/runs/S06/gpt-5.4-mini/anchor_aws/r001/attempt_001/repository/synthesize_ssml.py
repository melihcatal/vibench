from speech_client import get_client, get_config
from speech_models import audio_response, normalize_ssml_payload


def synthesize_ssml(payload, config=None):
    cfg = get_config(config)
    data = normalize_ssml_payload(payload)
    client = get_client(cfg)
    response = client.synthesize_speech(
        Text=data["ssml"],
        TextType="ssml",
        OutputFormat=cfg.get("output_format", "mp3"),
        VoiceId=data.get("voice_id", cfg.get("voice_id", "Joanna")),
        Engine=data.get("engine", cfg.get("engine", "neural")),
    )
    stream = response["AudioStream"]
    try:
        return audio_response(stream.read(), "audio/mpeg")
    finally:
        stream.close()
