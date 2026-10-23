import boto3

from translation_client import get_polly_client


def localized_audio_preview(payload, config=None):
    client = get_polly_client(config)
    response = client.synthesize_speech(
        Text=payload["text"],
        OutputFormat="mp3",
        VoiceId="Joanna",
        Engine="neural",
    )
    return {"audio_stream": response["AudioStream"].read()}
