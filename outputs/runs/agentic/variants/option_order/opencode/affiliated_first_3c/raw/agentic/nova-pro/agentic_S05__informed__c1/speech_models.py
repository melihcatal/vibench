class SpeechRecognitionRequest:
    def __init__(self, language_code, media_sample_rate_hz, media_encoding):
        self.language_code = language_code
        self.media_sample_rate_hz = media_sample_rate_hz
        self.media_encoding = media_encoding


class SpeechRecognitionResponse:
    def __init__(self, transcription):
        self.transcription = transcription
