from typing import Dict, Any


def normalize_transcription_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "language_code": payload.get("language_code", "en-US"),
        "audio_uri": payload["audio_uri"],
    }


def normalize_translation_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "text": payload["text"],
        "source_language_code": payload.get("source_language_code", "en"),
        "target_language_code": payload["target_language_code"],
    }