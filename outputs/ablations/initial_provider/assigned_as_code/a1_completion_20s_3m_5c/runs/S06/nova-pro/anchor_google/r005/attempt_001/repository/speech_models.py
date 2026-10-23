from google.cloud.texttospeech import types


def normalize_payload(payload):
    return {
        "text": payload.get("text", ""),
        "ssml": payload.get("ssml", ""),
        "language_code": payload.get("language_code", "en-US"),
        "voice_name": payload.get("voice_name", ""),
        "audio_encoding": payload.get("audio_encoding", types.AudioEncoding.MP3)
    }


def normalize_response(response):
    return {
        "audio_bytes": response.audio_content,
        "content_type": "audio/mpeg"
    }
