import boto3
import os
from database_client import get_translate_client
from database_models import TranslatedDocument

def translate_document_field(document_id: str, text_content: str, source_language: str, target_language: str) -> TranslatedDocument:
    """
    Translates user-facing document fields using AWS Translate.
    """
    translate_client = get_translate_client()
    try:
        response = translate_client.translate_text(
            Text=text_content,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        translated_text = response.get('TranslatedText')
        return TranslatedDocument(
            document_id=document_id,
            original_field=text_content,
            translated_text=translated_text,
            target_language=target_language
        )
    except Exception as e:
        print(f"Error translating document field with AWS Translate: {e}")
        raise
