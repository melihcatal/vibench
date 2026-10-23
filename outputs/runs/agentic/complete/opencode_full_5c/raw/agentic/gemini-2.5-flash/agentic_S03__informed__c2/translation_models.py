from typing import List, Dict, Union

# Define request and response models for clarity


class TranslationRequest:
    def __init__(
        self,
        text: Union[str, List[str]],
        target_language: str,
        source_language: str = None,
        format: str = "text",
    ):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language
        self.format = format  # 'text' or 'html'


class TranslationResponse:
    def __init__(
        self,
        original_text: Union[str, List[str]],
        translated_text: Union[str, List[str]],
        detected_source_language: str = None,
    ):
        self.original_text = original_text
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language


def normalize_response(google_cloud_response: dict) -> TranslationResponse:
    """Normalizes Google Cloud Translation API response to a common TranslationResponse model."""
    translated_text = google_cloud_response.get("translatedText")
    original_text = google_cloud_response.get("input")
    detected_source_language = google_cloud_response.get("detectedSourceLanguage")
    return TranslationResponse(
        original_text=original_text,
        translated_text=translated_text,
        detected_source_language=detected_source_language,
    )


def normalize_batch_response(
    google_cloud_responses: List[dict], original_texts: List[str]
) -> List[TranslationResponse]:
    """Normalizes a list of Google Cloud Translation API responses for batch translation."""
    normalized_responses = []
    for i, response in enumerate(google_cloud_responses):
        translated_text = response.get("translatedText")
        detected_source_language = response.get("detectedSourceLanguage")
        normalized_responses.append(
            TranslationResponse(
                original_text=original_texts[i],
                translated_text=translated_text,
                detected_source_language=detected_source_language,
            )
        )
    return normalized_responses
