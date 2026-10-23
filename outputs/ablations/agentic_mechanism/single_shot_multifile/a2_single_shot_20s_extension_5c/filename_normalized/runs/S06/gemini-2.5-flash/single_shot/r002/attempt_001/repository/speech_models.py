from dataclasses import dataclass
from google.cloud import texttospeech

@dataclass
class TextSynthesisRequest:
    text: str
    voice_name: str = "en-US-Wavenet-C"
    language_code: str = "en-US"
    gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.NEUTRAL
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0
    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3
    sample_rate_hertz: int = 24000

@dataclass
class AudioOutputConfig:
    audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3
    sample_rate_hertz: int = 24000
