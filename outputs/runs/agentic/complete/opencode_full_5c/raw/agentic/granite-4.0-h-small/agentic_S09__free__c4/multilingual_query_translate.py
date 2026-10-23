import webfetch


def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a query string into the target language before multilingual embedding search.
    Uses a public translation API (placeholder URL). Returns the translated query.
    """
    # Example placeholder translation service endpoint
    endpoint = "https://api.fake-translation-service.com/translate"
    payload = {"q": query, "target": target_lang}
    response = webfetch.fetch(url=endpoint, json=payload, format="text")
    # Assume the service echoes back the translated text in the body
    return response.text.strip()
