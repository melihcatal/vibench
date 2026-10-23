from google.cloud.texttospeech import types


def normalize_payload(payload):
    return {
        "text": payload.get("text", ""),
        "ssml": payload.get("ssml", ""),
        "language_code": payload.get("language_code", "en-US")
    }


def normalize_response(response):
    return {
        "audio_bytes": response.audio_content,
        "content_type": response.audio_config.audio_encoding
    }