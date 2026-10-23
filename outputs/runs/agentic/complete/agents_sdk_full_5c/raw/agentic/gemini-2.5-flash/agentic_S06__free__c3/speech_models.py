from typing import Optional, List
from enum import Enum
from google.cloud import texttospeech

class AudioEncoding(str, Enum):
    """Supported audio encoding formats."""
    LINEAR16 = "LINEAR16"
    MP3 = "MP3"
    OGG_OPUS = "OGG_OPUS"

class SsmlGender(str, Enum):
    """Supported SSML voice genders."""
    NEUTRAL = "NEUTRAL"
    MALE = "MALE"
    FEMALE = "FEMALE"

class VoiceParams:
    """Defines parameters for voice selection."""
    def __init__(self, language_code: str, ssml_gender: Optional[SsmlGender] = None, name: Optional[str] = None):
        self.language_code = language_code
        self.ssml_gender = ssml_gender
        self.name = name

    def to_texttospeech_voice_selection_params(self) -> texttospeech.VoiceSelectionParams:
        """Converts to Google Cloud Text-to-Speech VoiceSelectionParams."""
        params = {"language_code": self.language_code}
        if self.ssml_gender:
            params["ssml_gender"] = getattr(texttospeech.SsmlVoiceGender, self.ssml_gender.value)
        if self.name:
            params["name"] = self.name
        return texttospeech.VoiceSelectionParams(**params)

class SynthesisRequest:
    """Defines a request for text-to-speech synthesis."""
    def __init__(self,
                 text: Optional[str] = None,
                 ssml: Optional[str] = None,
                 voice_params: VoiceParams = VoiceParams("en-US", SsmlGender.NEUTRAL),
                 audio_encoding: AudioEncoding = AudioEncoding.MP3):
        if not text and not ssml:
            raise ValueError("Either 'text' or 'ssml' must be provided.")
        if text and ssml:
            raise ValueError("Only one of 'text' or 'ssml' can be provided.")

        self.text = text
        self.ssml = ssml
        self.voice_params = voice_params
        self.audio_encoding = audio_encoding

    def to_texttospeech_synthesis_input(self) -> texttospeech.SynthesisInput:
        """Converts to Google Cloud Text-to-Speech SynthesisInput."""
        if self.text:
            return texttospeech.SynthesisInput(text=self.text)
        else:
            return texttospeech.SynthesisInput(ssml=self.ssml)

    def to_texttospeech_audio_config(self) -> texttospeech.AudioConfig:
        """Converts to Google Cloud Text-to-Speech AudioConfig."""
        return texttospeech.AudioConfig(
            audio_encoding=getattr(texttospeech.AudioEncoding, self.audio_encoding.value)
        )

class VoiceInfo:
    """Represents information about an available voice."""
    def __init__(self, name: str, language_codes: List[str], ssml_gender: SsmlGender, natural_sample_rate_hertz: int):
        self.name = name
        self.language_codes = language_codes
        self.ssml_gender = ssml_gender
        self.natural_sample_rate_hertz = natural_sample_rate_hertz

    @classmethod
    def from_texttospeech_voice(cls, voice: texttospeech.Voice) -> "VoiceInfo":
        """Creates VoiceInfo from a Google Cloud Text-to-Speech Voice object."""
        return cls(
            name=voice.name,
            language_codes=list(voice.language_codes),
            ssml_gender=SsmlGender[texttospeech.SsmlVoiceGender(voice.ssml_gender).name],
            natural_sample_rate_hertz=voice.sample_rate_hertz
        )

if __name__ == '__main__':
    # Example usage
    # voice_params = VoiceParams("en-US", SsmlGender.FEMALE, "en-US-Wavenet-F")
    # print(f"VoiceParams: {voice_params.language_code}, {voice_params.ssml_gender}, {voice_params.name}")
    #
    # request = SynthesisRequest(text="Hello world.", voice_params=voice_params, audio_encoding=AudioEncoding.MP3)
    # print(f"SynthesisRequest: {request.text}, {request.audio_encoding}")
    #
    # # Demonstrate conversion to GCTS objects
    # gcts_voice_params = voice_params.to_texttospeech_voice_selection_params()
    # print(f"GCTS VoiceSelectionParams: {gcts_voice_params}")
    pass
