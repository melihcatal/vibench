import boto3

def summarize_moderation_decisions(text):
    comprehend = boto3.client('comprehend')
    summary = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return summary['Sentiment']