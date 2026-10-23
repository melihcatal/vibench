class TranscriptionRequest:
    def __init__(self, file_path):
        self.file_path = file_path

class TranscriptionResponse:
    def __init__(self, transcript):
        self.transcript = transcript