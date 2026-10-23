import os
import tempfile
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError


def generate_audio_brief(
    search_results: List[Dict[str, Any]], output_format: str = "mp3"
) -> str:
    """Generate a spoken brief from retrieved search results using Amazon Polly."""
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

    brief_text = "Search results summary. "

    if not search_results:
        brief_text += "No results found."
    else:
        brief_text += f"Found {len(search_results)} results. "

        for i, result in enumerate(search_results[:3], 1):
            if "title" in result:
                brief_text += f"Result {i}: {result['title']}. "
            if "snippet" in result and result["snippet"]:
                snippet = result["snippet"][:100]
                brief_text += f"{snippet}. "
            if "score" in result:
                score = result["score"]
                brief_text += f"Relevance score: {score:.2f}. "

    brief_text += "End of summary."

    try:
        response = polly_client.synthesize_speech(
            Text=brief_text,
            OutputFormat=output_format,
            VoiceId="Joanna",
            Engine="neural",
        )

        with tempfile.NamedTemporaryFile(
            suffix=f".{output_format}", delete=False
        ) as temp_file:
            temp_file.write(response["AudioStream"].read())
            audio_file_path = temp_file.name

        return audio_file_path

    except ClientError as e:
        raise Exception(f"Amazon Polly error: {str(e)}")
