from typing import Dict, Any


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "text": payload["text"],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "text": response["TranslatedText"],
        "source_language": response["SourceLanguageCode"],
        "target_language": response["TargetLanguageCode"],
    }