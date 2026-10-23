from google.cloud import texttospeech


def normalize_response(response):
    return {'audio_bytes': response.audio_content, 'content_type': 'audio/mpeg'}