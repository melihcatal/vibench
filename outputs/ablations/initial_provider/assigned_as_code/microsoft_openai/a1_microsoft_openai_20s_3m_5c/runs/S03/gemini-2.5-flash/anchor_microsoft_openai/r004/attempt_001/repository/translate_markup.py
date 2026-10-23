from translation_client import AzureTranslationClient
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse

def translate_markup(html: str, source_language: str, target_language: str, config: dict = None) -> MarkupTranslationResponse:
    config = config or {}
    client = AzureTranslationClient(api_key=config.get("api_key"), region=config.get("region"))
    request = MarkupTranslationRequest(html=html, source_language=source_language, target_language=target_language)
    response = client.translate_markup(request)
    return response
