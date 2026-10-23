import boto3
from storage_client import get_translate_client
from storage_models import TranslateRequest

def translate_stored_text(request: TranslateRequest) -> str:
    translate_client = get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code,
        )
        return response['TranslatedText']
    except translate_client.exceptions.ClientError as e:
        raise RuntimeError(f"Amazon Translate failed: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during translation: {e}")
