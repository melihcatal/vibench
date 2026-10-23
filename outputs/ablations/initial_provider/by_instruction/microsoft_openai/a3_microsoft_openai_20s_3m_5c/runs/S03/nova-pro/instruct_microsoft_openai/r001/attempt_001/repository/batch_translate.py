from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse, normalize_response

async def batch_translate(texts, target_language):
    client = TranslationClient()
    requests = [TranslationRequest(text, target_language) for text in texts]
    responses = await client.client.translate(requests)
    return [normalize_response(response) for response in responses]