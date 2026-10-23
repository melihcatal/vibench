# [HELPER] translation_models.py


class TranslationRequest:
    """Helper class for building translation requests."""

    def __init__(self, source_text: str, target_language: str = "es"):
        self.source_text = source_text
        self.target_language = target_language

    def to_dict(self):
        return {"source": self.source_text, "target": self.target_language}


class TranslationResponse:
    """Helper class to normalise responses from the translation client."""

    def __init__(self, raw_response):
        self.raw = raw_response
        self.translated_text = raw_response.get("translatedText")
        self.source = raw_response.get("original")
        self.detected_source_language = raw_response.get("detectedSourceLanguage")


def normalize_translation_response(raw):
    """Convert a raw client response into a TranslationResponse object."""
    return TranslationResponse(raw)
