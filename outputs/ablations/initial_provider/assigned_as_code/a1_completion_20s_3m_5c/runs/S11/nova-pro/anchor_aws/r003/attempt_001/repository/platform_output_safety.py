import boto3

def check_platform_output_safety(output):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=output,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return False
    return True