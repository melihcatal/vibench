class TranscriptionRequest:
    def __init__(self, audio_file_path):
        self.audio_file_path = audio_file_path


class TranscriptionResponse:
    def __init__(self, text):
        self.text = text
