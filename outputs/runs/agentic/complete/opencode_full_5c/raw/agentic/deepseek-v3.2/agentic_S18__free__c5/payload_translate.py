import os
from google.cloud import translate_v2 as translate


def payload_translate(payload, target_language="en", source_language=None):
    """Translate customer-facing message payload text using Google Cloud Translation API."""
    client = translate.Client()

    if isinstance(payload, dict):
        translated_payload = {}
        for key, value in payload.items():
            if isinstance(value, str) and key not in ["id", "timestamp", "metadata"]:
                try:
                    result = client.translate(
                        value,
                        target_language=target_language,
                        source_language=source_language,
                    )
                    translated_payload[key] = result["translatedText"]
                except Exception:
                    translated_payload[key] = value
            else:
                translated_payload[key] = value

        return {
            "translated_payload": translated_payload,
            "target_language": target_language,
            "source_language": source_language or "auto",
            "translation_service": "google-cloud-translate-v2",
        }

    elif isinstance(payload, str):
        try:
            result = client.translate(
                payload,
                target_language=target_language,
                source_language=source_language,
            )
            return {
                "original_text": payload,
                "translated_text": result["translatedText"],
                "detected_language": result.get("detectedSourceLanguage", "unknown"),
                "target_language": target_language,
                "translation_service": "google-cloud-translate-v2",
            }
        except Exception as e:
            return {
                "error": str(e),
                "original_text": payload,
                "target_language": target_language,
            }

    else:
        return {
            "error": "Payload must be dict or string",
            "payload_type": type(payload).__name__,
        }
