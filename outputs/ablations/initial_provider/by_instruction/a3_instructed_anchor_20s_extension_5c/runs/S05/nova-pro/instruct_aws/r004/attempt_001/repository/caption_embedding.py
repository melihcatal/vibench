import boto3

def caption_embedding(caption):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_key_phrases(Text=caption, LanguageCode='en')
    return response['KeyPhrases']