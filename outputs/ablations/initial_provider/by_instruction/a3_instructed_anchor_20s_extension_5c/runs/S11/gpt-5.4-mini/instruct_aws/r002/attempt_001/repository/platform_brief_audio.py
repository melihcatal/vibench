import boto3
from model_client import aws_region


def platform_brief_audio(text, voice_id="Joanna"):
    client = boto3.client("polly", region_name=aws_region())
    return client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id, Engine="neural")
