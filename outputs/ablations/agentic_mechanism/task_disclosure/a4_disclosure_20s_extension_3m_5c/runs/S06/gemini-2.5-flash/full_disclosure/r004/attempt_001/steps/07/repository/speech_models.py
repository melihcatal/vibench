
class SynthesizeRequest:
    def __init__(self, text, voice_id, audio_format="MP3", speaking_rate=1.0, pitch=0.0):
        self.text = text
        self.voice_id = voice_id
        self.audio_format = audio_format
        self.speaking_rate = speaking_rate
        self.pitch = pitch

class SynthesizeResponse:
    def __init__(self, audio_content):
        self.audio_content = audio_content

def normalize_text(text):
    # Basic text normalization: trim whitespace, remove extra spaces
    return " ".join(text.split()).strip()
