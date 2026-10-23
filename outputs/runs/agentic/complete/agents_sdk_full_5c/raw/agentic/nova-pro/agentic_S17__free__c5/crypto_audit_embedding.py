import boto3

def embed_crypto_audit(text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_dominant_language(Text=text)
    return response['Languages'][0]['LanguageCode']