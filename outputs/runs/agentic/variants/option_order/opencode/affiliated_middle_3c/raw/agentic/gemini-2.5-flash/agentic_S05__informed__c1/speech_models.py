class RecognitionResult:
    def __init__(self, transcript, is_final, language=None):
        self.transcript = transcript
        self.is_final = is_final
        self.language = language

    def to_dict(self):
        return {
            "transcript": self.transcript,
            "is_final": self.is_final,
            "language": self.language,
        }


class AudioChunk:
    def __init__(self, data, mimetype="audio/wav"):
        self.data = data
        self.mimetype = mimetype

    def to_bytes(self):
        return self.data
