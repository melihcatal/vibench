import os
import boto3
from typing import BinaryIO

def reviewer_brief_audio(brief: str, output: BinaryIO) -> None:
    polly = boto3.client(
        &quot;polly&quot;,
        aws_access_key_id=os.getenv(&quot;AWS_ACCESS_KEY_ID&quot;),
        aws_secret_access_key=os.getenv(&quot;AWS_SECRET_ACCESS_KEY&quot;),
        region_name=&quot;us-east-1&quot;
    )
    response = polly.synthesize_speech(
        Text=brief,
        OutputFormat=&quot;mp3&quot;,
        VoiceId=&quot;Joanna&quot;,
        Engine=&quot;neural&quot;
    )
    audio_stream = response[&quot;AudioStream&quot;]
    output.write(audio_stream.read())