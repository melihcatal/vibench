import boto3

def embed_caption(caption):
    client = boto3.client('comprehend')
    result = client.detect_dominant_language(Text=caption)
    return result['Languages'][0]['LanguageCode']