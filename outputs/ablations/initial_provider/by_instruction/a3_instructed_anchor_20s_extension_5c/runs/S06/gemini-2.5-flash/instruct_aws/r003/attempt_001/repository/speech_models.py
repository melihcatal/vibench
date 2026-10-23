from dataclasses import dataclass

@dataclass
class SynthesisRequest:
    text: str
    voice_id: str = "Joanna"
    output_format: str = "mp3"
    text_type: str = "text"

@dataclass
class SynthesisResponse:
    audio_stream: bytes
    content_type: str

@dataclass
class VoiceInfo:
    gender: str
    id: str
    language_code: str
    language_name: str
    name: str
    supported_engines: list[str]
