class TTSRequest:
    def __init__(self, text, ssml, voice_id, output_format):
        self.text = text
        self.ssml = ssml
        self.voice_id = voice_id
        self.output_format = output_format

class TTSResponse:
    def __init__(self, audio_stream):
        self.audio_stream = audio_stream