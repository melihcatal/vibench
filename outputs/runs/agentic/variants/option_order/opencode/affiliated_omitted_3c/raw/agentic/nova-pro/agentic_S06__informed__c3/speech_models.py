class TextToSpeechRequest:
    def __init__(self, text, voice=None):
        self.text = text
        self.voice = voice


class TextToSpeechResponse:
    def __init__(self, audio_data):
        self.audio_data = audio_data
