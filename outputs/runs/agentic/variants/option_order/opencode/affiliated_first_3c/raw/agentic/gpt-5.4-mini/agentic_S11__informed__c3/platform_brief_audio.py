import boto3
from model_models import PlatformResponse


def platform_brief_audio(response: PlatformResponse) -> bytes:
    client = boto3.client("polly")
    result = client.synthesize_speech(Text=response.text, OutputFormat="mp3", VoiceId="Joanna")
    return result["AudioStream"].read()
