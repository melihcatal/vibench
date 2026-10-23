import boto3

def live_caption_safety(caption):
    comprehend = boto3.client('comprehend', region_name='us-west-2')
    result = comprehend.detect_sentiment(Text=caption, LanguageCode='en')
    return result['Sentiment']