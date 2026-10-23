from google.cloud import texttospeech

def normalize_response(response):
    return response.audio_content