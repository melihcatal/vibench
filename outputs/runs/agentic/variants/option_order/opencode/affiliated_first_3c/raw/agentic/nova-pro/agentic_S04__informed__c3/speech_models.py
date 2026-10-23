class TranscriptionRequest:
    def __init__(self, file_uri):
        self.file_uri = file_uri


class TranscriptionResponse:
    def __init__(self, transcript):
        self.transcript = transcript
