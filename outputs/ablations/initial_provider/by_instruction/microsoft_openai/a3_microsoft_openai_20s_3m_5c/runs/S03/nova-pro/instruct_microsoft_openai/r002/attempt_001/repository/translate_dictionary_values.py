from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

endpoint = 'https://api.cognitive.microsofttranslator.com'
key = 'your-azure-key'

client = TranslationClient(endpoint, key)

def translate_dictionary_values(source_language: str, target_language: str, dictionary: Dict[str, str]) -> Dict[str, str]:
    translated_dictionary = {}
    for key, value in dictionary.items():
        request = TranslationRequest(source_language, target_language, value)
        response = client.translate(request.source_language, request.target_language, request.content)
        translated_dictionary[key] = TranslationResponse(response).translated_content
    return translated_dictionary