from typing import Optional, Literal

class TextSynthesisRequest:
    def __init__(self, text: str, voice_id: str, output_format: Literal['mp3', 'ogg', 'pcm'] = 'mp3'):
        self.text = text
        self.voice_id = voice_id
        self.output_format = output_format

class SsmlSynthesisRequest:
    def __init__(self, ssml: str, language_code: str, voice_name: str, speaking_rate: float = 1.0):
        self.ssml = ssml
        self.language_code = language_code
        self.voice_name = voice_name
        self.speaking_rate = speaking_rate

class VoiceSelectionParams:
    def __init__(self, locale: str, gender: Optional[Literal['Male', 'Female']] = None):
        self.locale = locale
        self.gender = gender

class AudioOutput:
    def __init__(self, audio_bytes: bytes, content_type: str = 'audio/mpeg'):
        self.audio_bytes = audio_bytes
        self.content_type = content_type

class TranslationRequest:
    def __init__(self, text: str, target_lang: str, source_lang: Optional[str] = None):
        self.text = text
        self.target_lang = target_lang
        self.source_lang = source_lang

class ModerationRequest:
    def __init__(self, text: str):
        self.text = text

class EmbeddingRequest:
    def __init__(self, texts: list[str]):
        self.texts = texts

class TranscriptionRequest:
    def __init__(self, audio_filepath: str):
        self.audio_filepath = audio_filepath
