import boto3

from speech_client import create_polly_client, resolve_output_format, resolve_voice_id


def synthesize_text(text: str, voice_id: str | None = None, output_format: str | None = None) -> bytes:
    client = create_polly_client()
    response = client.synthesize_speech(
        Text=text,
        VoiceId=resolve_voice_id(voice_id) or "Joanna",
        OutputFormat=resolve_output_format(output_format),
    )
    return response["AudioStream"].read()
