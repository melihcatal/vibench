import boto3
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse


def translate_stored_text(request: StoredTextTranslateRequest) -> StoredTextTranslateResponse:
    client = boto3.client("translate")
    resp = client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language or "auto",
        TargetLanguageCode=request.target_language,
    )
    return StoredTextTranslateResponse(
        source_language=request.source_language,
        target_language=request.target_language,
        translated_text=resp.get("TranslatedText", ""),
        provider="aws-translate",
    )
