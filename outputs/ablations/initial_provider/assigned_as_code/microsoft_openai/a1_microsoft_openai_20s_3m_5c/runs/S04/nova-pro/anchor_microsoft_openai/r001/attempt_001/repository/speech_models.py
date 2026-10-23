from.speech_models import NormalizeResponse


class TranscriptionRequest:
    def __init__(self, language_code, audio_uri):
        self.language_code = language_code
        self.audio_uri = audio_uri


class TranscriptionResponse:
    def __init__(self, text):
        self.text = text


def normalize_transcription_response(response):
    return NormalizeResponse(response)