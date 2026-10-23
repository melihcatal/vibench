from typing import Dict, Any


def normalize_translation_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "text": response["TranslatedText"],
        "source_language": response["SourceLanguageCode"],
        "target_language": response["TargetLanguageCode"],
    }
