def translate_request(text: str, source_lang: str, target_lang: str) -> dict:
    """Create request payload for Google Translate API.",
    """
    return {
        'q': text,
        'source': source_lang,
        'target': target_lang,
        'format': 'text'
    }

def normalize_response(response: dict) -> str:
    """Extract translated text from Google Translate API response.",
    """
    return response.get('translatedText', '')