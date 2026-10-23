import boto3


def secret_audit_embedding(payload, config=None):
    client = boto3.client('comprehend', region_name=config.get('region'))
    response = client.detect_sentiment(Text=payload['audit_note'], LanguageCode='en')
    return {'sentiment': response['Sentiment']}