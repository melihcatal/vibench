import boto3
from speech_models import ModerationRequest
import os

def moderate_transcript_text(request: ModerationRequest) -> dict:
    # AWS Comprehend Client
    region = os.environ.get("AWS_REGION", "us-east-1")
    comprehend_client = boto3.client("comprehend", region_name=region)
    
    response = comprehend_client.detect_sentiment(
        Text=request.text,
        LanguageCode='en' # Assuming English for moderation
    )
    return {
        "sentiment": response['Sentiment'],
        "sentiment_score": response['SentimentScore']
    }
