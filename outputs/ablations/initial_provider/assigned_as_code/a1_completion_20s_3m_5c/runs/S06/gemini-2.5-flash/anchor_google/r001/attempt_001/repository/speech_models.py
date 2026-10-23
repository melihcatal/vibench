class SynthesisInput:
    def __init__(self, text=None, ssml=None):
        if text is not None and ssml is not None:
            raise ValueError("Provide either text or ssml, not both.")
        self.text = text
        self.ssml = ssml


class VoiceConfig:
    def __init__(self, language_code="en-US", name=None, ssml_gender="NEUTRAL"):
        self.language_code = language_code
        self.name = name
        self.ssml_gender = ssml_gender


class AudioConfig:
    def __init__(self,
        audio_encoding="MP3",
        speaking_rate=1.0,
        pitch=0.0,
        volume_gain_db=0.0,
        sample_rate_hertz=None,
    ):
        self.audio_encoding = audio_encoding
        self.speaking_rate = speaking_rate
        self.pitch = pitch
        self.volume_gain_db = volume_gain_db
        self.sample_rate_hertz = sample_rate_hertz


class SynthesisResponse:
    def __init__(self, audio_content, content_type="audio/mpeg"):
        self.audio_content = audio_content
        self.content_type = content_type


class VoiceSelectionResponse:
    def __init__(self,
        name,
        language_codes,
        ssml_gender,
        natural_sample_rate_hertz,
    ):
        self.name = name
        self.language_codes = language_codes
        self.ssml_gender = ssml_gender
        self.natural_sample_rate_hertz = natural_sample_rate_hertz