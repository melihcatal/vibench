from typing import List, Dict, Any

# This file can be used to define common data models or utility functions
# for request/response normalization across different translation operations.

class TranslationRequest:
    def __init__(self, text_content: str, target_language: str, source_language: str = "en", mime_type: str = "text/plain"):
        self.text_content = text_content
        self.target_language = target_language
        self.source_language = source_language
        self.mime_type = mime_type

class TranslationResponse:
    def __init__(self, translated_text: str, detected_source_language: str = None):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language

def normalize_batch_response(api_response: Any) -> List[str]:
    """Normalizes a batch translation API response to a list of strings."""
    return [translation.translated_text for translation in api_response.translations]

def denormalize_dictionary_request(data: Dict[str, Any]) -> Dict[str, str]:
    """Extracts string values from a dictionary for translation."""
    extracted_strings = {}
    for key, value in data.items():
        if isinstance(value, str):
            extracted_strings[key] = value
    return extracted_strings

