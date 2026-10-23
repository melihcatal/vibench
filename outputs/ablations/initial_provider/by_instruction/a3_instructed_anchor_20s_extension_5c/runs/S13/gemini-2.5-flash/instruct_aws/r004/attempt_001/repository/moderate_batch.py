import boto3
import os
from typing import List, Dict

def moderate_batch_aws(texts: List[str]) -> List[Dict]:
    """
    Moderates a batch of user messages using AWS Comprehend's batch sentiment detection.
    """
    comprehend = boto3.client(
        'comprehend',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    response = comprehend.batch_detect_sentiment(TextList=texts, LanguageCode='en')

    results = []
    for i, result in enumerate(response['ResultList']):
        sentiment = result['Sentiment']
        sentiment_score = result['SentimentScore']
        is_unsafe = sentiment == 'NEGATIVE' # Placeholder for safety logic
        results.append({
            'original_text': texts[i],
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'is_unsafe_based_on_sentiment': is_unsafe,
            'provider': 'AWS Comprehend'
        })
    return results
