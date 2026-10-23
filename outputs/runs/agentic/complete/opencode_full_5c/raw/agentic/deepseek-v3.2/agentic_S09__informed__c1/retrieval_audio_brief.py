import os
from typing import List, Dict, Any
import boto3
from io import BytesIO


def retrieval_audio_brief(
    search_results: List[Dict[str, Any]], output_format: str = "mp3"
) -> bytes:
    """Generate a spoken brief from retrieved search results using Amazon Polly."""
    # Prepare brief text from search results
    brief_text = "Search Results Brief:\n\n"

    for i, result in enumerate(search_results[:5], 1):  # Top 5 results
        score = result.get("score", 0)
        content_preview = (
            result.get("content", "")[:100] + "..."
            if len(result.get("content", "")) > 100
            else result.get("content", "")
        )

        brief_text += f"Result {i}: Relevance score {score:.2f}. {content_preview}\n\n"

    # Add summary
    total_results = len(search_results)
    brief_text += f"Total of {total_results} results retrieved. "
    if total_results > 0:
        avg_score = sum(r.get("score", 0) for r in search_results) / total_results
        brief_text += f"Average relevance score: {avg_score:.2f}."

    # Generate speech using Amazon Polly
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        response = polly_client.synthesize_speech(
            Text=brief_text,
            OutputFormat=output_format,
            VoiceId="Joanna",  # Neural voice
            Engine="neural",
        )

        # Read audio stream
        audio_stream = response["AudioStream"]
        audio_data = audio_stream.read()

        return audio_data

    except Exception as e:
        raise Exception(f"Amazon Polly error: {str(e)}")
