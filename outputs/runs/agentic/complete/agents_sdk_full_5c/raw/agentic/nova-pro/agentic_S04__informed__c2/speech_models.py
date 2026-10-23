class TranscriptionRequest:
    def __init__(self, audio_file_path, speaker_labels=False):
        self.audio_file_path = audio_file_path
        self.speaker_labels = speaker_labels

class TranscriptionResponse:
    def __init__(self, text, status, speaker_labels=None, words=None):
        self.text = text
        self.status = status
        self.speaker_labels = speaker_labels
        self.words = words