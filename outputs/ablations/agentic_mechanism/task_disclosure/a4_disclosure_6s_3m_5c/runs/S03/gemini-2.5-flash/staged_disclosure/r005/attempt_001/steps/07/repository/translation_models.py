
class TranslationRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language

class TranslationResponse:
    def __init__(self, translated_text: str, detected_source_language: str = None):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language

def normalize_translation_response(response_data: dict) -> TranslationResponse:
    """
    Normalizes a dictionary response from a translation service into a TranslationResponse object.
    Assumes response_data contains 'translatedText' and optionally 'detectedSourceLanguage'.
    """
    translated_text = response_data.get("translatedText")
    detected_source_language = response_data.get("detectedSourceLanguage")

    if translated_text is None:
        raise ValueError("Translation response data is missing 'translatedText'.")

    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language=detected_source_language
    )
