import os
import boto3
from storage_client import get_translate_client
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse

def translate_stored_text(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    translate_client = get_translate_client()

    # AWS Translate `translate_text` performs text translation
    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language,
        TargetLanguageCode=request.target_language
    )

    translated_text = response.get('TranslatedText', '')

    return StoredTextTranslateResponse(translated_text=translated_text)
