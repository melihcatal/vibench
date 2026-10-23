import os
import boto3
from typing import List, Dict, Any
from botocore.exceptions import ClientError


def generate_audio_brief(
    search_results: List[Dict[str, Any]], output_format: str = "mp3"
) -> bytes:
    """
    Generate a spoken brief from retrieved search results using Amazon Polly.

    Args:
        search_results: List of search result dictionaries with 'text' and 'score' keys
        output_format: Audio format (mp3, ogg_vorbis, pcm)

    Returns:
        Audio data as bytes
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    polly_client = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    if not search_results:
        brief_text = "No search results found."
    else:
        top_results = sorted(
            search_results, key=lambda x: x.get("score", 0), reverse=True
        )[:3]

        brief_parts = [
            f"Found {len(search_results)} search results. Here are the top {len(top_results)}:"
        ]

        for i, result in enumerate(top_results, 1):
            text_preview = result.get("text", "")[:100]
            if len(result.get("text", "")) > 100:
                text_preview += "..."
            score = result.get("score", 0)
            brief_parts.append(
                f"Result {i}: {text_preview} Relevance score: {score:.2f}"
            )

        brief_text = " ".join(brief_parts)

    try:
        response = polly_client.synthesize_speech(
            Text=brief_text,
            OutputFormat=output_format,
            VoiceId="Joanna",
            Engine="neural",
        )

        if "AudioStream" in response:
            audio_data = response["AudioStream"].read()
            return audio_data
        else:
            raise ValueError("No audio stream in Polly response")

    except ClientError as e:
        raise Exception(f"Amazon Polly error: {e}")


def save_audio_brief(audio_data: bytes, filename: str = "search_brief.mp3") -> str:
    """
    Save audio brief to file.

    Args:
        audio_data: Audio data bytes from generate_audio_brief
        filename: Output filename

    Returns:
        Path to saved file
    """
    with open(filename, "wb") as f:
        f.write(audio_data)

    return filename


def create_search_summary_text(search_results: List[Dict[str, Any]]) -> str:
    """
    Create a text summary of search results for audio synthesis.

    Args:
        search_results: List of search result dictionaries

    Returns:
        Text summary suitable for text-to-speech
    """
    if not search_results:
        return "No search results found."

    total_results = len(search_results)
    avg_score = (
        sum(r.get("score", 0) for r in search_results) / total_results
        if total_results > 0
        else 0
    )

    top_results = sorted(search_results, key=lambda x: x.get("score", 0), reverse=True)[
        :3
    ]

    summary_parts = [
        f"Search completed with {total_results} results.",
        f"Average relevance score: {avg_score:.2f}.",
        "Top results:",
    ]

    for i, result in enumerate(top_results, 1):
        text_preview = result.get("text", "")[:80]
        if len(result.get("text", "")) > 80:
            text_preview += "..."
        score = result.get("score", 0)
        summary_parts.append(f"Result {i}: {text_preview} Score: {score:.2f}")

    return " ".join(summary_parts)
