import boto3
from database_client import get_s3_client

def translate_text(text, source_language, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return response.TranslatedText