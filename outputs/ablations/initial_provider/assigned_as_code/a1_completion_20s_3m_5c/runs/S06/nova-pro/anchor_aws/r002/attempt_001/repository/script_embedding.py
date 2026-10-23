import boto3


def embed_script(script):
    client = boto3.client('comprehend')
    response = client.detect_dominant_language(Text=script)
    return response['Languages'][0]['LanguageCode']