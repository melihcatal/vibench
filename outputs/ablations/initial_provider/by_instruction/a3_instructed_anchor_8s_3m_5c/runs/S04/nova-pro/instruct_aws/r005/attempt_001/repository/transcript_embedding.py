import boto3

def embed_transcript(transcript_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_dominant_language(Text=transcript_text)
    return response['Languages'][0]['LanguageCode']