import boto3

comprehend = boto3.client('comprehend')

def safety_threshold(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment_score = response['SentimentScore']
    if sentiment_score['Negative'] > 0.5:
        return False
    return True
