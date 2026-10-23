import boto3

from storage_client import get_s3_client


def translate_text(text, source_language_code, target_language_code, config=None):
    config = config or {}
    translate_client = boto3.client('translate', region_name=config.get('region'))

    response = translate_client.translate_text(Text=text, SourceLanguageCode=source_language_code, TargetLanguageCode=target_language_code)
    return response['TranslatedText']