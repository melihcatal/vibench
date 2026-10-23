import boto3
from document_client import get_translate_client

def ocr_translate(text, source_language, target_language):
    translate_client = get_translate_client()
    response = translate_client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return response['TranslatedText']