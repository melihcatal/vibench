import boto3

def summarize_transcript(transcript_uri):
    comprehend = boto3.client('comprehend')
    with open(transcript_uri, 'r') as file:
        transcript_text = file.read()
    response = comprehend.detect_sentiment(Text=transcript_text, LanguageCode='en')
    return response.get('Sentiment')