class TranscriptionRequest:
    def __init__(self, audio_file):
        self.audio_file = audio_file


class TranscriptionResponse:
    def __init__(self, results):
        self.results = results
