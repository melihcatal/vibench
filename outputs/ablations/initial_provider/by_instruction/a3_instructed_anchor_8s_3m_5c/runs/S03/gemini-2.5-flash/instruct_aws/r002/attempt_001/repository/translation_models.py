from dataclasses import dataclass

@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str

@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str

def normalize_text_input(text_input: str) -> str:
    """
    Normalizes text input for translation.
    """
    return text_input.strip()

def parse_translation_response(response: dict) -> TranslationResponse:
    """
    Parses the AWS Translate response into a TranslationResponse object.
    """
    return TranslationResponse(
        translated_text=response["TranslatedText"],
        source_language=response["SourceLanguageCode"],
        target_language=response["TargetLanguageCode"]
    )
