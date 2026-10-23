import os

import boto3


def moderate_transcript(text: str, language_code: str = 'en') -> dict:
    client = boto3.client('comprehend', region_name=os.getenv('AWS_REGION', os.getenv('AWS_DEFAULT_REGION', 'us-east-1')))
    moderation = client.detect_dominant_language(Text=text)
    entities = client.detect_key_phrases(Text=text, LanguageCode=language_code)
    return {'dominant_language': moderation, 'key_phrases': entities}
