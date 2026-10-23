from safety_client import get_polly_client
from safety_models import normalize_text


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    client = get_polly_client(config)
    text = normalize_text(payload.get("text"))
    response = client.synthesize_speech(
        Text=text,
        OutputFormat=config.get("output_format", "mp3"),
        VoiceId=config.get("voice_id", "Joanna"),
    )
    return {"audio_stream": response.get("AudioStream")}
