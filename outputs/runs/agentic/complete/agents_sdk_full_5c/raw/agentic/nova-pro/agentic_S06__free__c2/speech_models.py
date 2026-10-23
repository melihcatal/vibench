class SpeechSynthesisRequest:
    def __init__(self, text, voice_id='Joanna', output_format='mp3'):
        self.text = text
        self.voice_id = voice_id
        self.output_format = output_format

class SpeechSynthesisResponse:
    def __init__(self, audio_stream):
        self.audio_stream = audio_stream