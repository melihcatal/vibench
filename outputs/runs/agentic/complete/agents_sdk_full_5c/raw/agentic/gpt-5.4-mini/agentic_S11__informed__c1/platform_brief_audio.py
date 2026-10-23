from typing import Optional

import boto3


def platform_brief_audio(text: str, voice_id: str = "Joanna", output_format: str = "mp3", region_name: Optional[str] = None) -> bytes:
    client = boto3.client("polly", region_name=region_name)
    response = client.synthesize_speech(Text=text, OutputFormat=output_format, VoiceId=voice_id, Engine="neural")
    return response["AudioStream"].read()
