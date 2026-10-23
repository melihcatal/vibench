class SynthesisPayload:
    def __init__(self, text=None, ssml=None, voice_name=None, output_format=None):
        if text and ssml:
            raise ValueError("Cannot provide both text and ssml.")
        if not (text or ssml):
            raise ValueError("Must provide either text or ssml.")
        self.text = text
        self.ssml = ssml
        self.voice_name = voice_name
        self.output_format = output_format

class AudioResult:
    def __init__(self, audio_data, content_type):
        self.audio_data = audio_data
        self.content_type = content_type