import boto3

def profile_moderation(text):
    comprehend = boto3.client('comprehend')
    result = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    if result['Sentiment']!= 'POSITIVE':
        raise ValueError('Profile text sentiment is not positive')
    return result['Sentiment']