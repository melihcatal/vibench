from typing import Optional
from dataclasses import dataclass
from storage_client import get_translate_client

@dataclass
class StoredTextTranslateRequest:
    text: str
    source_language_code: str # e.g., "en"
    target_language_code: str # e.g., "es"

@dataclass
class StoredTextTranslateResponse:
    success: bool
    message: str
    translated_text: Optional[str] = None
    source_language_code: Optional[str] = None
    target_language_code: Optional[str] = None

def translate_stored_text(
    request: StoredTextTranslateRequest
) -> StoredTextTranslateResponse:
    """
    Translates text extracted from a stored document using AWS Translate.
    """
    translate_client = get_translate_client()

    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language_code,
            TargetLanguageCode=request.target_language_code
        )

        translated_text = response.get("TranslatedText")
        source_language_code = response.get("SourceLanguageCode")
        target_language_code = response.get("TargetLanguageCode")

        return StoredTextTranslateResponse(
            success=True,
            message="Text translated successfully",
            translated_text=translated_text,
            source_language_code=source_language_code,
            target_language_code=target_language_code
        )
    except Exception as e:
        return StoredTextTranslateResponse(success=False, message=f"Error translating text: {str(e)}")
