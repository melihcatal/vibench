import boto3

def check_script_for_unsafe_content(script):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(
        Text=script,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return True
    return False