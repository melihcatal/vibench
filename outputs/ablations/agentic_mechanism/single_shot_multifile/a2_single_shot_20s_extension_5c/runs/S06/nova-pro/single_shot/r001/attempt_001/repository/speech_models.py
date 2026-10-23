class TTSRequest:
    def __init__(self, text, ssml):
        self.text = text
        self.ssml = ssml

class TTSResponse:
    def __init__(self, audio_content):
        self.audio_content = audio_content