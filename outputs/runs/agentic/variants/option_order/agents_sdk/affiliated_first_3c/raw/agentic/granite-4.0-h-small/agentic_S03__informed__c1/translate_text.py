# [SAME-SCENARIO] translate_text.py

from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

def translate_text(source_text: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translate a single text string using a concrete provider.

    Uses Google Cloud Translation as the provider. Credentials are expected in
    environment variable GOOGLE_APPLICATION_CREDENTIALS.
    """
    client = TranslationClient()
    request = TranslationRequest(
        model_id="general",  # Google's general translation model
        source_lang=source_lang,
        target_lang=target_lang,
        source_text=source_text
    )
    response: TranslationResponse = client.translate(request)
    return response.translated_text

# Example usage (removed in production builds)
# if __name__ == "__main__":
#     print(translate_text("Hello world", source_lang='en', target_lang='fr'))
