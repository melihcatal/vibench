import boto3


def metric_annotation_safety(payload, config=None):
    config = config or {}
    client = boto3.client('comprehend', region_name=config.get('region', 'us-east-1'))
    response = client.detect_sentiment(
        Text=payload['text'],
        LanguageCode='en'
    )
    return {'safety': response['Sentiment']}