import boto3

comprehend = boto3.client('comprehend')

def summarize_transcription(transcript):
    response = comprehend.detect_sentiment(Text=transcript, LanguageCode='en')
    return response['Sentiment']