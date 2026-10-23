from speech_client import get_client, stream_to_bytes, load_config
from speech_models import normalize_ssml_payload, build_audio_response


def synthesize_ssml(payload, config=None):
    cfg = load_config(config)
    client = get_client(cfg)
    response = client.synthesize_speech(
        Text=normalize_ssml_payload(payload),
        TextType="ssml",
        OutputFormat=cfg.get("output_format", "mp3"),
        VoiceId=cfg.get("voice_id", "Joanna"),
        LanguageCode=cfg.get("language_code"),
    )
    return build_audio_response(stream_to_bytes(response["AudioStream"]), "audio/mpeg")
