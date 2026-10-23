class SpeechRequest:
    def __init__(self, text, text_type, output_format, voice_id):
        self.text = text
        self.text_type = text_type
        self.output_format = output_format
        self.voice_id = voice_id


class SpeechResponse:
    def __init__(self, audio_bytes, content_type):
        self.audio_bytes = audio_bytes
        self.content_type = content_type