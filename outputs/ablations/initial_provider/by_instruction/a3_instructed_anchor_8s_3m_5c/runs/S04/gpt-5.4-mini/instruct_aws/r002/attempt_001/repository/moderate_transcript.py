import boto3

from speech_client import load_config


def moderate_transcript(text: str) -> dict:
    config = load_config()
    client = boto3.client(
        "comprehend",
        region_name=config.aws_region,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
    )
    return client.detect_sentiment(Text=text, LanguageCode="en")
