# [SAME-SCENARIO] translate_dictionary_values.py

from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

def translate_dictionary_values(data: dict, source_lang: str = 'en', target_lang: str = 'es') -> dict:
    """Translate all string values in a dictionary while preserving keys.

    Uses Google Cloud Translation for each string value. Provider: Google Cloud Translation.
    Credentials via GOOGLE_APPLICATION_CREDENTIALS.
    """
    client = TranslationClient()
    result = {}
    for key, value in data.items():
        if isinstance(value, str):
            request = TranslationRequest(model_id="general", source_lang=source_lang, target_lang=target_lang, source_text=value)
            response: TranslationResponse = client.translate(request)
            result[key] = response.translated_text
        elif isinstance(value, dict):
            # Recurse into nested dictionaries
            result[key] = translate_dictionary_values(value, source_lang, target_lang)
        else:
            result[key] = value  # non-string values unchanged
    return result

# Example usage (removed in production)
#if __name__ == "__main__":
#    sample = {"greeting": "Hello", "farewell": "Goodbye", "nested": {"msg": "See you"}}
#    print(translate_dictionary_values(sample))
