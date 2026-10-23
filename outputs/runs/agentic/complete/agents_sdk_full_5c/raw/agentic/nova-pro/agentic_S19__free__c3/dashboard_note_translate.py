import boto3
from observability_client import get_translate_client

translate = get_translate_client()

def translate_dashboard_note(text, source_language, target_language):
    response = translate.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response['TranslatedText']