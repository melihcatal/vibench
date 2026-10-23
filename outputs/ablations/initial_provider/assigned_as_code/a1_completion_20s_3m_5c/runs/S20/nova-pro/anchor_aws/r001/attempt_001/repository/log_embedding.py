import boto3

import observability_client


def log_embedding(log_message):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=log_message,
        LanguageCode='en',
    )
    return response['Sentiment']