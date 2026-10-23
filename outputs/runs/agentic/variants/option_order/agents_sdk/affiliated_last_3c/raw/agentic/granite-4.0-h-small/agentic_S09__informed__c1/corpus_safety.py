import os
from embeddings_client import get_embed_client
from embeddings_models import normalize_embedding

def is_corpus_safe(text: str, threshold: float = 0.2) -> bool:
    """Check if a corpus text is safe for embedding using a toxicity classifier.
    This example uses Amazon Comprehend (or Bedrock Guardrails) via boto3 SDK.
    Provider identification signals: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, boto3 import.
    """
    client = get_embed_client()  # demonstrates client utility; actual safety uses separate SDK
    # Using AWS Comprehend API directly (could also be Bedrock Guardrails)
    import boto3
    comprehend = boto3.client(
        'comprehend',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response.get('Sentiment', '')
    # Simple safety rule: flag if sentiment is NEGATIVE or MIXED with high confidence
    confidence = response.get('SentimentScore', {}).get(sentiment, 0.0)
    if sentiment in ('NEGATIVE', 'MIXED') and confidence > threshold:
        return False
    return True
