import boto3


def summarize_onboarding_state(user_id, config=None):
    config = config or {}
    client = boto3.client('comprehend', region_name=config.get('region'))
    response = client.detect_sentiment(Text=user_id, LanguageCode='en')
    return response['Sentiment']
