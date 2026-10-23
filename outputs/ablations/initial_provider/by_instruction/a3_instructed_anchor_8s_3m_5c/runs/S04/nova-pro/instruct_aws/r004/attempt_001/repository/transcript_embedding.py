import boto3

def transcript_embedding(transcript_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_dominant_language(Text=transcript_text)
    return response