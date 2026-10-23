from elevenlabs import Voice, Audio


class SpeechRequest:
    def __init__(self, text: str, voice: Voice):
        self.text = text
        self.voice = voice


class SpeechResponse:
    def __init__(self, audio: Audio):
        self.audio = audio
