class SpeechRequest:
    def __init__(self, text, voice_id="Joanna"):
        self.text = text
        self.voice_id = voice_id


class SpeechResponse:
    def __init__(self, audio_stream):
        self.audio_stream = audio_stream
