import os
import json
from typing import Dict, Any, Optional
from google.cloud import translate_v2 as translate


def translate_payload_text(
    payload: Dict[str, Any],
    target_language: str = "en",
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set for Google Cloud Translation"
        )

    client = translate.Client()

    translated_payload = payload.copy()

    def translate_text_fields(obj):
        if isinstance(obj, str):
            if obj.strip() and len(obj.strip()) > 3:
                try:
                    result = client.translate(
                        obj,
                        target_language=target_language,
                        source_language=source_language,
                    )
                    return result["translatedText"]
                except Exception as e:
                    print(
                        f"Failed to translate text with Google Cloud Translation: {e}"
                    )
                    return obj
            return obj
        elif isinstance(obj, dict):
            return {k: translate_text_fields(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [translate_text_fields(item) for item in obj]
        else:
            return obj

    try:
        translated_payload = translate_text_fields(payload)

        print(
            f"Translated payload to {target_language} using Google Cloud Translation API"
        )

        return {
            "original_payload": payload,
            "translated_payload": translated_payload,
            "target_language": target_language,
            "source_language": source_language or "auto",
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        print(f"Failed to translate payload with Google Cloud Translation: {e}")
        raise


def translate_customer_facing_text(
    payload: Dict[str, Any], customer_language: str = "en"
) -> Dict[str, Any]:
    text_fields_to_translate = [
        "content",
        "message",
        "description",
        "title",
        "comment",
        "feedback",
    ]

    translated = payload.copy()

    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set for Google Cloud Translation"
        )

    client = translate.Client()

    def translate_field(value, field_path=""):
        if isinstance(value, str):
            if any(field in field_path.lower() for field in text_fields_to_translate):
                if value.strip() and len(value.strip()) > 3:
                    try:
                        result = client.translate(
                            value, target_language=customer_language
                        )
                        return result["translatedText"]
                    except Exception as e:
                        print(
                            f"Failed to translate field {field_path} with Google Cloud Translation: {e}"
                        )
                        return value
            return value
        elif isinstance(value, dict):
            return {
                k: translate_field(v, f"{field_path}.{k}" if field_path else k)
                for k, v in value.items()
            }
        elif isinstance(value, list):
            return [
                translate_field(item, f"{field_path}[{i}]")
                for i, item in enumerate(value)
            ]
        else:
            return value

    try:
        translated = translate_field(translated)

        print(
            f"Translated customer-facing text to {customer_language} using Google Cloud Translation"
        )

        return {
            "original": payload,
            "translated": translated,
            "customer_language": customer_language,
            "translated_fields": text_fields_to_translate,
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        print(
            f"Failed to translate customer-facing text with Google Cloud Translation: {e}"
        )
        raise


def detect_payload_language(payload: Dict[str, Any]) -> Dict[str, Any]:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set for Google Cloud Translation"
        )

    client = translate.Client()

    text_samples = []

    def collect_text_samples(obj):
        if isinstance(obj, str):
            if obj.strip() and len(obj.strip()) > 10:
                text_samples.append(obj.strip())
        elif isinstance(obj, dict):
            for v in obj.values():
                collect_text_samples(v)
        elif isinstance(obj, list):
            for item in obj:
                collect_text_samples(item)

    collect_text_samples(payload)

    if not text_samples:
        return {
            "detected_language": "unknown",
            "confidence": 0,
            "text_samples": 0,
            "provider": "Google Cloud Translation",
        }

    sample_text = text_samples[0][:100]

    try:
        result = client.detect_language(sample_text)

        print(
            f"Detected language using Google Cloud Translation: {result['language']} (confidence: {result.get('confidence', 0)})"
        )

        return {
            "detected_language": result["language"],
            "confidence": result.get("confidence", 0),
            "text_samples": len(text_samples),
            "sample_text": sample_text,
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        print(f"Failed to detect language with Google Cloud Translation: {e}")
        return {
            "detected_language": "unknown",
            "confidence": 0,
            "text_samples": len(text_samples),
            "provider": "Google Cloud Translation",
            "error": str(e),
        }


if __name__ == "__main__":
    sample_payload = {
        "user_id": "user_123",
        "action": "post_comment",
        "content": "Este es un producto excelente. Me encanta usarlo todos los días.",
        "rating": 5,
        "metadata": {
            "title": "Mi reseña",
            "description": "Una reseña positiva sobre el producto",
        },
    }

    try:
        print("Detecting language:")
        lang_result = detect_payload_language(sample_payload)
        print(
            f"Detected: {lang_result['detected_language']} (confidence: {lang_result['confidence']})"
        )

        print("\nTranslating to English:")
        translate_result = translate_payload_text(sample_payload, target_language="en")
        print(f"Original content: {sample_payload['content'][:50]}...")
        print(
            f"Translated content: {translate_result['translated_payload']['content'][:50]}..."
        )

        print("\nTranslating customer-facing text to French:")
        customer_result = translate_customer_facing_text(
            sample_payload, customer_language="fr"
        )
        print(f"Original title: {sample_payload['metadata']['title']}")
        print(f"Translated title: {customer_result['translated']['metadata']['title']}")

    except Exception as e:
        print(f"Error: {e}")
