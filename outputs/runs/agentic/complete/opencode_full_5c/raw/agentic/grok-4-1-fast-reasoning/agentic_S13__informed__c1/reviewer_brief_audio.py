import os
import boto3
from safety_models import SafetyResult


def generate_reviewer_brief_audio(
    brief_text: str, output_file: str = "reviewer_brief.mp3"
) -> str:
    polly = boto3.client(
        "polly",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1",
    )
    response = polly.synthesize_speech(
        Text=brief_text, OutputFormat="mp3", VoiceId="Joanna", Engine="neural"
    )
    with open(output_file, "wb") as file:
        file.write(response["AudioStream"].read())
    return output_file


def generate_from_result(
    result: SafetyResult, output_file: str = "reviewer_brief.mp3"
) -> str:
    brief = f"Moderation result for text: {result.original_text[:100]}... Blocked: {result.blocked}. Reason: {result.rationale}"
    return generate_reviewer_brief_audio(brief, output_file)
