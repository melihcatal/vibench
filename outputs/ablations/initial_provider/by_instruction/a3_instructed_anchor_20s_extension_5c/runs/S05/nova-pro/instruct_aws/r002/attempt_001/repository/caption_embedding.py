import boto3

def caption_embedding(caption):
    comprehend = boto3.client('comprehend', region_name='us-west-2')
    result = comprehend.detect_sentiment(Text=caption, LanguageCode='en')
    return result['Sentiment']