from speech_client import get_client, load_config
from speech_models import audio_response, normalize_ssml_payload


def synthesize_ssml(payload, config=None):
    cfg = load_config(config)
    client = get_client(cfg)
    data = normalize_ssml_payload(payload)
    response = client.synthesize_speech(
        Text=data["ssml"],
        TextType="ssml",
        OutputFormat=cfg["output_format"],
        VoiceId=data.get("voice_id", cfg["voice_id"]),
        LanguageCode=cfg["language_code"] if cfg["language_code"] else None,
    )
    stream = response["AudioStream"]
    try:
        return audio_response(stream.read(), f"audio/{cfg['output_format']}")
    finally:
        stream.close()
