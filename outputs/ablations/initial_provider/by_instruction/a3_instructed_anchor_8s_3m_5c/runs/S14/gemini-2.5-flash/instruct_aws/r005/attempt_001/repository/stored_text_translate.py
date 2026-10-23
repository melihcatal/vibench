import boto3
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse

def get_translate_client():
    return boto3.client('translate')

def stored_text_translate(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    translate_client = get_translate_client()

    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language,
        TargetLanguageCode=request.target_language
    )

    return StoredTextTranslateResponse(translated_text=response['TranslatedText'])
