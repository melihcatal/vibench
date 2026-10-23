import boto3

def moderate_transcript(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return 'Moderation required: Negative sentiment detected.'
    else:
        return 'Transcript approved.'