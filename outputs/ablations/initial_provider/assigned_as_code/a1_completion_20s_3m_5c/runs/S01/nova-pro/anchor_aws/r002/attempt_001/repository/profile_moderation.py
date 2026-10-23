import boto3


def profile_moderation(text):
    comprehend = boto3.client('comprehend', region_name='us-west-2')
    result = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return result['Sentiment']