import boto3

def summarize_transcription(transcript_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=transcript_text, LanguageCode='en')
    return response['Sentiment']