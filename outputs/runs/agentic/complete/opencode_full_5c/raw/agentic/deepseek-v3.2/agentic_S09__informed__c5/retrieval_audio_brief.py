import os
import boto3
from typing import List, Dict, Any


def generate_audio_brief(
    search_results: List[Dict[str, Any]], output_format: str = "mp3"
) -> bytes:
    """Generate a spoken brief from retrieved search results using Amazon Polly."""
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION", "us-east-1")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    polly_client = boto3.client(
        "polly",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    summary_text = (
        f"Search results summary. Found {len(search_results)} relevant documents. "
    )

    for i, result in enumerate(search_results[:3], 1):
        title = result.get("title", "Untitled")
        snippet = result.get("snippet", "")[:100]
        summary_text += f"Result {i}: {title}. {snippet}. "

    if len(search_results) > 3:
        summary_text += f"Plus {len(search_results) - 3} more results."

    try:
        response = polly_client.synthesize_speech(
            Text=summary_text,
            OutputFormat=output_format,
            VoiceId="Joanna",
            Engine="neural",
        )

        if "AudioStream" in response:
            audio_data = response["AudioStream"].read()
            return audio_data
        else:
            raise Exception("No audio stream in response")

    except Exception as e:
        raise Exception(f"Audio synthesis failed: {str(e)}")
