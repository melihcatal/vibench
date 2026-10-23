import boto3

def embed_transcript(transcript_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_sentiment(Text=transcript_text, LanguageCode='en')
    return response.get('Sentiment')