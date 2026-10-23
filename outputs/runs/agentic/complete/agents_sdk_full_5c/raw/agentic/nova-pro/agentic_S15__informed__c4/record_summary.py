import boto3

def summarize_record(text):
    comprehend = boto3.client('comprehend', region_name='us-west-2', aws_access_key_id='YOUR_AWS_ACCESS_KEY_ID', aws_secret_access_key='YOUR_AWS_SECRET_ACCESS_KEY')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment']