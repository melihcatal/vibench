class SynthesisInput:
    def __init__(self, text=None, ssml=None):
        self.text = text
        self.ssml = ssml

class VoiceSelectionParams:
    def __init__(self, language_code, ssml_gender):
        self.language_code = language_code
        self.ssml_gender = ssml_gender

class AudioConfig:
    def __init__(self, audio_encoding):
        self.audio_encoding = audio_encoding