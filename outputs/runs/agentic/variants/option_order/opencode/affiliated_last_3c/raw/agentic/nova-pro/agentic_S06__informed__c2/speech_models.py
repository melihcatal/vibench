from google.cloud.texttospeech import types


def normalize_response(response):
    return response.audio_content
