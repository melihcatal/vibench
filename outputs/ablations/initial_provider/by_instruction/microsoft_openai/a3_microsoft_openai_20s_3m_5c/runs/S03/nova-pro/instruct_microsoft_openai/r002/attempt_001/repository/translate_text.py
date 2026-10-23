from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

endpoint = 'https://api.cognitive.microsofttranslator.com'
key = 'your-azure-key'

client = TranslationClient(endpoint, key)

def translate_text(source_language: str, target_language: str, text: str) -> str:
    request = TranslationRequest(source_language, target_language, text)
    response = client.translate(request.source_language, request.target_language, request.content)
    return TranslationResponse(response).translated_content