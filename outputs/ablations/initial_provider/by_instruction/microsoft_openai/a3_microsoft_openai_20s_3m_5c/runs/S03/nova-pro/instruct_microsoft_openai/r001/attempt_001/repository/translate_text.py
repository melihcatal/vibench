from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse, normalize_response

async def translate_text(text, target_language):
    client = TranslationClient()
    request = TranslationRequest(text, target_language)
    response = await client.client.translate([request])
    return normalize_response(response[0])