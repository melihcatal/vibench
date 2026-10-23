import boto3

comprehend_client = boto3.client('comprehend')

def embed_script(text):
    response = comprehend_client.detect_dominant_language(Text=text)
    return response['Languages'][0]['LanguageCode']