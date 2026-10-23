from document_client import DocumentClient
from document_models import TranslationRequest, TranslationResponse
import logging

logger = logging.getLogger(__name__)

def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = DocumentClient()
    translate_client = client.translate_client

    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code
    )

    return TranslationResponse(
        translated_text=response['TranslatedText'],
        source_language_code=response['SourceLanguageCode'],
        target_language_code=response['TargetLanguageCode']
    )
