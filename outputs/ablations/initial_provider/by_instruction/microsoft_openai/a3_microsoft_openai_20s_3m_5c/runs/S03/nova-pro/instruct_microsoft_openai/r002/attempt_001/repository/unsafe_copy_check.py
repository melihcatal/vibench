from translation_client import TranslationClient

endpoint = 'https://api.cognitive.microsofttranslator.com'
key = 'your-azure-key'

client = TranslationClient(endpoint, key)

def check_unsafe_copy(text: str) -> bool:
    # Placeholder for actual implementation
    return False