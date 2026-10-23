import boto3

def live_caption_safety(caption):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=caption, LanguageCode='en')
    return response['Sentiment']