from google.cloud import texttospeech


def normalize_request(text):
    return texttospeech.SynthesisInput(text=text)


def normalize_response(response):
    return response.audio_content
