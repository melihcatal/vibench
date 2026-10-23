class SpeechRequest:
    def __init__(self, text, voice_name=None):
        self.text = text
        self.voice_name = voice_name


class SpeechResponse:
    def __init__(self, audio_data):
        self.audio_data = audio_data
