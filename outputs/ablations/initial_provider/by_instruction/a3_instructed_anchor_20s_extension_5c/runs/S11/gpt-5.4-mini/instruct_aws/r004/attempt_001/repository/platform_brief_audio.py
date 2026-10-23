from typing import Any, Dict

import boto3


def platform_brief_audio(text: str) -> Dict[str, Any]:
    client = boto3.client("polly", region_name="us-east-1")
    return client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
