from speech_client import get_polly_client
from speech_models import normalize_ssml


def synthesize_ssml(
    ssml: str, voice_id: str = "Joanna", output_format: str = "mp3"
) -> bytes:
    ssml = normalize_ssml(ssml)
    client = get_polly_client()
    response = client.synthesize_speech(
        Text=ssml,
        TextType="ssml",
        OutputFormat=output_format,
        VoiceId=voice_id,
        Engine="neural",
    )
    return response["AudioStream"].read()
