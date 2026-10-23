import os
import boto3

def profile_moderation(text):
    client = boto3.client(
        'comprehend',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    try:
        # Detects entities for general moderation
        # For more specific moderation, custom classifiers or other services might be needed.
        response = client.detect_sentiment(
            Text=text,
            LanguageCode='en'
        )
        sentiment = response['Sentiment']
        sentiment_score = response['SentimentScore']

        # Simple example: if sentiment is 'NEGATIVE' or 'MIXED' it might need moderation
        if sentiment == 'NEGATIVE' or sentiment == 'MIXED':
            return {"moderation_status": "FLAGGED", "sentiment": sentiment, "score": sentiment_score}
        else:
            return {"moderation_status": "CLEAN", "sentiment": sentiment, "score": sentiment_score}
    except Exception as e:
        return {"error": str(e)}
