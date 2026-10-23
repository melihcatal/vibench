from google.cloud import translate
import dataclasses

@dataclasses.dataclass
class StoredTextTranslateRequest:
    text_content: str
    target_language: str
    source_language: str = 'en'

@dataclasses.dataclass
class StoredTextTranslateResponse:
    translated_text: str
    detected_source_language: str

def translate_stored_text(
    request: StoredTextTranslateRequest
) -> StoredTextTranslateResponse:
    """Translates text extracted from a stored document using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{client.project_path()}"

    response = client.translate_text(
        parent=parent,
        contents=[request.text_content],
        target_language_code=request.target_language,
        source_language_code=request.source_language,
    )

    translated_text = ""
    detected_source_language = ""

    if response.translations:
        translated_text = response.translations[0].translated_text
        detected_source_language = response.translations[0].detected_language_code

    return StoredTextTranslateResponse(
        translated_text=translated_text,
        detected_source_language=detected_source_language
    )
