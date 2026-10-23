class SpeechSynthesisRequest:
    def __init__(self, text, output_format='mp3', voice_id='Joanna'):
        self.text = text
        self.output_format = output_format
        self.voice_id = voice_id

class SpeechSynthesisResponse:
    def __init__(self, audio_stream):
        self.audio_stream = audio_stream