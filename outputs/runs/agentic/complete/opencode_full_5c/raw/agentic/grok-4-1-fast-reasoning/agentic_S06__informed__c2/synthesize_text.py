from speech_client import get_polly_client
from speech_models import normalize_text


def synthesize_text(
    text: str, voice_id: str = "Joanna", output_format: str = "mp3"
) -> bytes:
    text = normalize_text(text)
    client = get_polly_client()
    response = client.synthesize_speech(
        Text=text, OutputFormat=output_format, VoiceId=voice_id, Engine="neural"
    )
    return response["AudioStream"].read()
