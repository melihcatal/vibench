import boto3

def moderate_transcript(transcript):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=transcript, LanguageCode='en')
    sentiment = response['Sentiment']
    if sentiment == 'NEGATIVE':
        return '*** MODERATED CONTENT ***'
    else:
        return transcript