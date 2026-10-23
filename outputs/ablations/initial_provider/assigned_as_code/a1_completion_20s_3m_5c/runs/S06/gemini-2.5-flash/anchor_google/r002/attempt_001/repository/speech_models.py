from google.cloud import texttospeech

class SynthesisPayload:
    def __init__(self, text=None, ssml=None, language_code="en-US", voice_name=None, audio_encoding=texttospeech.AudioEncoding.MP3, speaking_rate=1.0, pitch=0.0):
        self.text = text
        self.ssml = ssml
        self.language_code = language_code
        self.voice_name = voice_name
        self.audio_encoding = audio_encoding
        self.speaking_rate = speaking_rate
        self.pitch = pitch

    def to_synthesis_input(self):
        if self.ssml:
            return texttospeech.SynthesisInput(ssml=self.ssml)
        return texttospeech.SynthesisInput(text=self.text)

    def to_voice_selection_params(self):
        return texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.voice_name
        )

    def to_audio_config(self):
        return texttospeech.AudioConfig(
            audio_encoding=self.audio_encoding,
            speaking_rate=self.speaking_rate,
            pitch=self.pitch
        )

class VoiceInfo:
    def __init__(self, name, language_codes, gender, natural_sample_rate_hertz):
        self.name = name
        self.language_codes = language_codes
        self.gender = gender
        self.natural_sample_rate_hertz = natural_sample_rate_hertz

    @classmethod
    def from_texttospeech_voice(cls, voice):
        return cls(
            name=voice.name,
            language_codes=voice.language_codes,
            gender=texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            natural_sample_rate_hertz=voice.natural_sample_rate_hertz
        )
