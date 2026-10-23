import boto3

def embed_script(text):
    comprehend_client = boto3.client('comprehend')
    result = comprehend_client.detect_dominant_language(Text=text)
    return result['Languages'][0]['LanguageCode']