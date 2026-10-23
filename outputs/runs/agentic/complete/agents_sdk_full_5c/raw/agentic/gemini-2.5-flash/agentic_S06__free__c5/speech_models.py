
from enum import Enum
from dataclasses import dataclass
from google.cloud import texttospeech_v1 as texttospeech

class AudioOutputFormat(Enum):
    MP3 = texttospeech.AudioEncoding.MP3
    LINEAR16 = texttospeech.AudioEncoding.LINEAR16
    OGG_OPUS = texttospeech.AudioEncoding.OGG_OPUS

class VoiceGender(Enum):
    FEMALE = texttospeech.SsmlVoiceGender.FEMALE
    MALE = texttospeech.SsmlVoiceGender.MALE
    NEUTRAL = texttospeech.SsmlVoiceGender.NEUTRAL
    UNSPECIFIED = texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED

@dataclass
class SynthesisRequest:
    text: str = None
    ssml: str = None
    voice_name: str = "en-US-Wavenet-D"
    language_code: str = "en-US"
    audio_format: AudioOutputFormat = AudioOutputFormat.MP3

    def to_text_to_speech_input(self) -> texttospeech.SynthesisInput:
        if self.text:
            return texttospeech.SynthesisInput(text=self.text)
        elif self.ssml:
            return texttospeech.SynthesisInput(ssml=self.ssml)
        else:
            raise ValueError("Either 'text' or 'ssml' must be provided for synthesis.")

    def to_voice_selection_params(self) -> texttospeech.VoiceSelectionParams:
        return texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.voice_name,
        )

    def to_audio_config(self) -> texttospeech.AudioConfig:
        return texttospeech.AudioConfig(
            audio_encoding=self.audio_format.value
        )

if __name__ == '__main__':
    # Example usage
    request = SynthesisRequest(
        text="Hello from speech models!",
        voice_name="en-US-Standard-C",
        language_code="en-US",
        audio_format=AudioOutputFormat.LINEAR16
    )

    print(f"Request Text: {request.text}")
    print(f"Request Voice Name: {request.voice_name}")
    print(f"Request Audio Format: {request.audio_format.name} ({request.audio_format.value})")
