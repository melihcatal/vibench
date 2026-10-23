import boto3

def embed_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_dominant_language(Text=text)
    return response['Languages'][0]['LanguageCode']