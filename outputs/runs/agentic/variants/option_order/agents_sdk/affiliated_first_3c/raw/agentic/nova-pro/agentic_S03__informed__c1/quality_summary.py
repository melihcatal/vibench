import boto3

def summarize_quality_issues(text):
    comprehend = boto3.client('comprehend')
    result = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return result['Sentiment']