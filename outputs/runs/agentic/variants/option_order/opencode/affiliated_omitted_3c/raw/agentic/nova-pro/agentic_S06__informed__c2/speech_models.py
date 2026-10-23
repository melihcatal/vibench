class SpeechRequest:
    def __init__(self, text, voice="en-US-Wavenet-D"):
        self.text = text
        self.voice = voice


class SpeechResponse:
    def __init__(self, audio_content):
        self.audio_content = audio_content
