from google.cloud.texttospeech import types

def normalize_payload(payload):
    return {
        "text": payload.get("text", ""),
        "language_code": payload.get("language_code", "en-US"),
        "audio_encoding": types.AudioEncoding.MP3
    }

def normalize_response(response):
    return {
        "audio_bytes": response.audio_content,
        "content_type": "audio/mpeg"
    }