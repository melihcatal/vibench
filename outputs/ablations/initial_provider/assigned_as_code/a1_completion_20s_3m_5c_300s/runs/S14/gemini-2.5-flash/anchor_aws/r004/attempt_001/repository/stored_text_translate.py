import boto3
from storage_client import get_translate_client
from storage_models import StorageConfig, TranslateRequest

def stored_text_translate(request: TranslateRequest, config: StorageConfig):
    translate_client = get_translate_client(config)
    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code
    )
    return {"translated_text": response['TranslatedText']}
