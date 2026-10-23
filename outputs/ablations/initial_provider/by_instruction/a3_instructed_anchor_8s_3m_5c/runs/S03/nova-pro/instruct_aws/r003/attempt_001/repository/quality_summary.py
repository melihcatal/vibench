import boto3

def summarize_quality_issues(translation):
    client = boto3.client('comprehend')
    result = client.detect_sentiment(Text=translation, LanguageCode='en')
    return result['Sentiment']