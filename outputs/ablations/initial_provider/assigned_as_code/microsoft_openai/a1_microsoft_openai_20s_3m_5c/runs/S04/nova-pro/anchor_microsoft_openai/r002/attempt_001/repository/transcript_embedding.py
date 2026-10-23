import boto3

comprehend = boto3.client('comprehend')

def transcript_embedding(text):
    response = comprehend.detect_dominant_language(Text=text)
    language_code = response['Languages'][0]['LanguageCode']
    return language_code