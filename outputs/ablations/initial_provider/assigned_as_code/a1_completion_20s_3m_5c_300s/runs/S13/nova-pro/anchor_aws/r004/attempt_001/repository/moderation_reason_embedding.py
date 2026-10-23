import boto3


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    client = boto3.client('comprehend', region_name=config.get('region', 'us-east-1'))
    response = client.detect_dominant_language(Text=payload['text'])
    language_code = response['Languages'][0]['LanguageCode']
    response = client.detect_sentiment(Text=payload['text'], LanguageCode=language_code)
    return {'sentiment': response['Sentiment']}