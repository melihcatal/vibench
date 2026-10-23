from dataclasses import dataclass
from typing import Optional
import google.cloud.texttospeech as tts

@dataclass
class VoiceParams:
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None  # e.g., 'FEMALE', 'MALE', 'NEUTRAL'

    def to_pb(self) -> tts.VoiceSelectionParams:
        gender = None
        if self.ssml_gender:
            gender = getattr(tts.SsmlVoiceGender, self.ssml_gender.upper(), None)
        return tts.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.name,
            ssml_gender=gender
        )

@dataclass
class AudioConfig:
    encoding: str = 'MP3'
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0

    def to_pb(self) -> tts.AudioConfig:
        encoding_enum = getattr(tts.AudioEncoding, self.encoding.upper())
        return tts.AudioConfig(
            audio_encoding=encoding_enum,
            speaking_rate=self.speaking_rate,
            pitch=self.pitch,
            volume_gain_db=self.volume_gain_db
        )

def create_speech_request(text_or_ssml: str, is_ssml: bool, voice_params: Optional[VoiceParams] = None,
                          audio_config: Optional[AudioConfig] = None) -> tts.SynthesizeSpeechRequest:
    if is_ssml:
        input_pb = tts.SynthesisInput(ssml=text_or_ssml)
    else:
        input_pb = tts.SynthesisInput(text=text_or_ssml)
    voice_pb = voice_params.to_pb() if voice_params else tts.VoiceSelectionParams(language_code='en-US')
    audio_pb = audio_config.to_pb() if audio_config else tts.AudioConfig()
    return tts.SynthesizeSpeechRequest(
        input=input_pb,
        voice=voice_pb,
        audio_config=audio_pb
    )
