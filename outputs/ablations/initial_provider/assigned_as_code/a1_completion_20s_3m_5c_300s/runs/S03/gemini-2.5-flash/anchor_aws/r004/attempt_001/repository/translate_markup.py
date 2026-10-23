import boto3
from translation_client import get_translate_client
from translation_models import TranslationRequest, TranslationResponse

def translate_markup(payload: TranslationRequest, config: dict = None) -> TranslationResponse:
    config = config or {}
    client = get_translate_client(config.get("region", "us-east-1"))

    response = client.translate_text(
        Text=payload.text,
        SourceLanguageCode=payload.source_language,
        TargetLanguageCode=payload.target_language,
        TextType='html'
    )
    return TranslationResponse(
        text=response["TranslatedText"],
        source_language=payload.source_language,
        target_language=payload.target_language,
    )
