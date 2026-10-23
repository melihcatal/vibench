from speech_client import client, load_config
from speech_models import normalize_ssml_payload, audio_result


def synthesize_ssml(payload, config=None):
    payload = normalize_ssml_payload(payload)
    cfg = load_config(config)
    polly = client(cfg)
    response = polly.synthesize_speech(Text=payload["ssml"], TextType="ssml", OutputFormat=cfg["output_format"], VoiceId=payload.get("voice_id", cfg["voice_id"]))
    stream = response["AudioStream"]
    try:
        return audio_result(stream.read(), "audio/mpeg")
    finally:
        stream.close()
