class SpeechRequest:
    def __init__(self, text, output_format="mp3", voice_id="Joanna", text_type="text"):
        self.text = text
        self.output_format = output_format
        self.voice_id = voice_id
        self.text_type = text_type


class SpeechResponse:
    def __init__(self, audio_stream):
        self.audio_stream = audio_stream
