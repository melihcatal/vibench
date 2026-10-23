"""
Generate spoken briefs for moderation reviewers using Amazon Polly.
"""
import os
import boto3
from typing import List
from safety_models import TextModerationResult


def generate_reviewer_brief(results: List[TextModerationResult], output_file: str) -> None:
    """Generate an audio brief for moderation reviewers using Amazon Polly."""
    polly = boto3.client(
        "polly",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    if not polly:
        raise ValueError("AWS credentials are required for Amazon Polly.")

    brief_text = "Moderation Review Brief:\n"
    for result in results:
        brief_text += f"Text: {result.text}\n"
        for score in result.scores:
            brief_text += f"{score.category}: {score.score:.2f}\n"
        brief_text += "\n"

    response = polly.synthesize_speech(
        Text=brief_text,
        OutputFormat="mp3",
        VoiceId="Joanna"
    )

    with open(output_file, "wb") as audio_file:
        audio_file.write(response["AudioStream"].read())