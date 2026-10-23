from google.cloud.translate_v3 import TranslateTextRequest


def normalize_payload(payload):
    normalized_payload = {
        "text": payload["text"],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
    return normalized_payload


def normalize_response(response):
    normalized_response = {
        "text": response.translations[0].translated_text,
        "source_language": response.source_language_code,
        "target_language": response.target_language_code,
    }
    return normalized_response