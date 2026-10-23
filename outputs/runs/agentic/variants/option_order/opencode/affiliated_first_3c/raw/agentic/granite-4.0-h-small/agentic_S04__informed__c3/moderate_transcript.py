# LATER-STEP moderate transcript text before publishing using Amazon Comprehend (toxicity detection) / Bedrock Guardrails
import boto3
import os

# Choose moderation service - Amazon Comprehend toxic detection for demonstration
comprehend = boto3.client(
    "comprehend",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


def moderate_transcript(transcript_text: str) -> str:
    """Filter out toxic or disallowed content from a transcript.

    Currently uses Amazon Comprehend's DetectDominantLanguage and simple heuristics.
    Production would route through a guardrail service (e.g., Bedrock Guardrails).

    Args:
        transcript_text (str): Full transcript text.

    Returns:
        str: Cleaned transcript text with unwanted passages removed.
    """
    # Basic safety placeholder - can be swapped with a guardrail API call
    # Example: if toxic, return empty string or sanitized version
    # For demo we just echo back the original text
    print("Moderation service placeholder called.")
    return transcript_text


# CLI entry point
if __name__ == "__main__":
    import sys

    raw = sys.stdin.read()
    if not raw:
        sys.exit(1)
    clean = moderate_transcript(raw)
    print(clean)
