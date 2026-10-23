class TranslationRequest:
    """Standardized request object used by same‑scenario translation functions."""
    def __init__(self, source: str, target: str, text: str):
        self.source = source
        self.target = target
        self.text = text

class TranslationResponse:
    """Standardized response object returned by same‑scenario helpers."""
    def __init__(self, translated_text: str, source_lang: str, target_lang: str, raw_response=None):
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.raw_response = raw_response  # keep provider‑specific data if needed

def build_payload(request: TranslationRequest, provider: str) -> dict:
    """Convert a TranslationRequest into a dict understood by the provider client.",
    provider = provider.lower()
    if provider == "deepl":
        return {"source_lang": request.source, "target_lang": request.target, "text": request.text}
    elif provider == "google":
        return {"source": request.source, "target": request.target, "text": request.text}
    elif provider == "amazon":
        return {"SourceLanguageCode": request.source, "TargetLanguageCode": request.target, "Text": request.text}
    elif provider == "alibaba":
        return {"SourceLanguage": request.source, "TargetLanguage": request.target, "Text": request.text}
    elif provider == "azure":
        return {
            "source_text": {"text": request.text},
            "target_language": request.target
        }
    elif provider == "watsonx":
        return {"source_lang": request.source, "target_lang": request.target, "text": request.text}
    raise ValueError(f"Unsupported provider for payload build: {provider}")

def parse_response(raw_response, provider: str) -> TranslationResponse:
    """Normalize a provider‑specific response into a TranslationResponse."""
    provider = provider.lower()
    if provider in ("deepl", "google", "amazon", "watsonx"):
        return TranslationResponse(
            translated_text=raw_response.get("translatedText"),
            source_lang=raw_response.get("detectedSourceLanguage"),
            target_lang=raw_response.get("target_lang")
        )
    elif provider == "azure":
        translation = raw_response.get("translation", [{}])[0]
        return TranslationResponse(
            translated_text=translation.get("text"),
            source_lang="unknown",
            target_lang=translation.get("to")
        )
    elif provider == "alibaba":
        return TranslationResponse(
            translated_text=raw_response.get("TranslatedText"),
            source_lang=raw_response.get("SourceLanguage"),
            target_lang=raw_response.get("TargetLanguage")
        )
    raise ValueError(f"Unsupported provider for parsing: {provider}")
