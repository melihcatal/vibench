import boto3

def embed_script(script):
    comprehend_client = boto3.client('comprehend')
    result = comprehend_client.detect_dominant_language(Text=script)
    return result['Languages'][0]['LanguageCode']