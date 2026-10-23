from typing import Optional

def translate_query(query: str, target_lang: str = "en") -> Optional[str]:
    """Translate a query string into the target language using a translation API.
    In a real implementation, call a hosted translation service (e.g., Google Translate, DeepL, or a cloud provider).
    Return None if translation fails or input is empty.
    """
    # Placeholder: replace with actual provider client (e.g., google-cloud-translate)
    try:
        from google.cloud import translate_v2 as translate
    except ImportError:
        raise ImportError("google-cloud-translate not installed. Install it for translation support.")
    client = translate.Client()
    if not query:
        return None
    result = client.translate(query, target_language=target_lang)
    # result['translatedText'] holds the translation
    return result.get('translatedText')
