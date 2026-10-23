from typing import Dict


def generate_reviewer_brief(moderation_data: Dict) -> Dict:
    """
    Generates spoken briefs for moderation reviewers using Amazon Polly.
    Provider: Amazon Polly
    Model: standard voice "Joanna"
    """
    import boto3
    import os

    polly = boto3.client(
        "polly",
        region_name=os.getenv("AWS_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    brief_text = (
        f"Moderation Review Brief. "
        f"Text: {moderation_data.get('text', 'N/A')}. "
        f"Decision: {'Allowed' if moderation_data.get('allowed', False) else 'Blocked'}. "
        f"Reason: {moderation_data.get('reason', 'N/A')}. "
        f"Categories Triggered: {', '.join(moderation_data.get('categories_triggered', []))}"
    )

    response = polly.synthesize_speech(
        Text=brief_text, OutputFormat="mp3", VoiceId="Joanna"
    )

    return {
        "audio_stream": response["AudioStream"].read(),
        "brief_text": brief_text,
        "voice": "Joanna",
    }
