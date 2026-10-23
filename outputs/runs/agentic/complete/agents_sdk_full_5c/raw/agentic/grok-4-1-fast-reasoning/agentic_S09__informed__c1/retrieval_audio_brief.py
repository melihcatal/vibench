import os
import boto3
from typing import List

def retrieval_audio_brief(retrieved_results: List[str], output_file: str = "brief.mp3") -> None:
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials required")
    polly = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1"
    )
    brief_text = "Here is a spoken brief of the retrieved search results: " + "; ".join(retrieved_results[:10])
    response = polly.synthesize_speech(
        Text=brief_text,
        OutputFormat="mp3",
        VoiceId="Joanna"
    )
    with open(output_file, "wb") as file:
        file.write(response["AudioStream"].read())
