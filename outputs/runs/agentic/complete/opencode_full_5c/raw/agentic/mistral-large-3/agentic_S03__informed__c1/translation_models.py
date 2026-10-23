from typing import Dict, List, Optional, TypedDict


class TranslationRequest(TypedDict, total=False):
    """
    Typed dictionary for translation request parameters.
    """

    Text: str
    SourceLanguageCode: str
    TargetLanguageCode: str
    Settings: Optional[Dict]


class TranslationResponse(TypedDict):
    """
    Typed dictionary for translation response.
    """

    TranslatedText: str
    SourceLanguageCode: str
    TargetLanguageCode: str
    AppliedSettings: Optional[Dict]


class LanguageInfo(TypedDict):
    """
    Typed dictionary for language information.
    """

    LanguageCode: str
    LanguageName: str


def normalize_text(text: str) -> str:
    """
    Normalizes text by stripping whitespace and handling empty strings.

    Args:
        text: The text to normalize.

    Returns:
        Normalized text or empty string if input is None/whitespace-only.
    """
    if not text:
        return ""
    return text.strip()


def normalize_language_code(language_code: str) -> str:
    """
    Normalizes language codes to lowercase and strips whitespace.

    Args:
        language_code: The language code to normalize (e.g., 'EN' or ' en ').

    Returns:
        Normalized language code (e.g., 'en').
    """
    if not language_code:
        raise ValueError("Language code cannot be empty")
    return language_code.strip().lower()


def validate_translation_request(request: TranslationRequest) -> None:
    """
    Validates a translation request.

    Args:
        request: The translation request to validate.

    Raises:
        ValueError: If the request is invalid.
    """
    if not request.get("Text"):
        raise ValueError("Text cannot be empty")
    if not request.get("SourceLanguageCode"):
        raise ValueError("Source language code cannot be empty")
    if not request.get("TargetLanguageCode"):
        raise ValueError("Target language code cannot be empty")
    if request["SourceLanguageCode"] == request["TargetLanguageCode"]:
        raise ValueError("Source and target language codes cannot be the same")
