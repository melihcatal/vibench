from speech_client import create_polly_client, resolve_output_format, resolve_voice_id


def synthesize_ssml(ssml: str, voice_id: str | None = None, output_format: str | None = None) -> bytes:
    client = create_polly_client()
    response = client.synthesize_speech(
        Text=ssml,
        TextType="ssml",
        VoiceId=resolve_voice_id(voice_id) or "Joanna",
        OutputFormat=resolve_output_format(output_format),
    )
    return response["AudioStream"].read()
