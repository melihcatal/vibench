import boto3

def check_script_safety(script):
    comprehend_client = boto3.client('comprehend')
    result = comprehend_client.detect_sentiment(Text=script, LanguageCode='en')
    return result['Sentiment']