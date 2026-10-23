import boto3

def embed_translated_segments(text):
    client = boto3.client('comprehend')
    result = client.detect_dominant_language(Text=text)
    return result['Languages'][0]['LanguageCode']