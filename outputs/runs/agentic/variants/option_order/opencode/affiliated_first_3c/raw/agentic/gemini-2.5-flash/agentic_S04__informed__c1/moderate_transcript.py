import os
import boto3
from speech_models import ModerationRequest


def moderate_transcript_text(request: ModerationRequest):
    comprehend_client = boto3.client(
        "comprehend",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # Using DetectSentiment as a basic moderation example.
    # For full content moderation, Amazon Comprehend has specific content moderation APIs
    # or one would integrate with AWS Rekognition for image/video or a dedicated moderation service.
    response = comprehend_client.detect_sentiment(Text=request.text, LanguageCode="en")
    return response
