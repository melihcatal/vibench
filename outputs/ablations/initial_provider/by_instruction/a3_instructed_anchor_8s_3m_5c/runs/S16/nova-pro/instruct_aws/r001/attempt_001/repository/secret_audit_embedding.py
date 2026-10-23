import boto3

def embed_secret_audit_notes(notes):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_dominant_language(Text=notes)
    return response['Languages'][0]['LanguageCode']