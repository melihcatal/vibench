import boto3

comprehend = boto3.client('comprehend')

def embed_text(text):
    response = comprehend.detect_dominant_language(Text=text)
    return response['Languages'][0]['LanguageCode']