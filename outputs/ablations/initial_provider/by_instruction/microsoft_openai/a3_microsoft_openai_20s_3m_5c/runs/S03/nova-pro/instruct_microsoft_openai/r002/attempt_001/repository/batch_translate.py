from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

endpoint = 'https://api.cognitive.microsofttranslator.com'
key = 'your-azure-key'

client = TranslationClient(endpoint, key)

def batch_translate(source_language: str, target_language: str, texts: List[str]) -> List[str]:
    translated_texts = []
    for text in texts:
        request = TranslationRequest(source_language, target_language, text)
        response = client.translate(request.source_language, request.target_language, request.content)
        translated_texts.append(TranslationResponse(response).translated_content)
    return translated_texts