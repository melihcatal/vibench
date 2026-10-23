class SpeechSynthesisRequest:
    def __init__(self, text):
        self.text = text

class SpeechSynthesisResponse:
    def __init__(self, audio_data):
        self.audio_data = audio_data