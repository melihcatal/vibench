# Define local request, response, and normalization helpers for Text-to-Speech

from dataclasses import dataclass
from typing import List, Optional, Union, Dict

@dataclass
class TTSVoice:
    name: str
    language_codes: List[str]
    ssml_gender: Optional[str] = None

@dataclass
class TTSAudioConfig:
    encoding: str = "MP3"
    sample_rate_hertz: Optional[int] = None
    speaking_rate: float = 1.0

@dataclass
class TTSRequest:
    input_data: Union[str, bytes]
    is_ssml: bool = False
    voice: Optional[TTSVoice] = None
    audio_config: Optional[TTSAudioConfig] = None

def normalize_tts_request(req: Dict) -> TTSRequest:
    return TTSRequest(
        input_data=req.get("input", ""),
        is_ssml=req.get("ssml", False),
        voice=TTSVoice(**req.get("voice", {})) if req.get("voice") else None,
        audio_config=TTSAudioConfig(**req.get("audio_config", {})) if req.get("audio_config") else None
    )
