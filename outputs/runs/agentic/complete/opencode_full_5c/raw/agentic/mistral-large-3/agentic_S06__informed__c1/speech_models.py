from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    audio_encoding: str = "LINEAR16"


@dataclass
class SynthesisResponse:
    audio_content: bytes


class SpeechNormalizer:
    @staticmethod
    def normalize_request(request: Dict[str, Any]) -> SynthesisRequest:
        return SynthesisRequest(
            text=request.get("text"),
            ssml=request.get("ssml"),
            language_code=request.get("language_code", "en-US"),
            voice_name=request.get("voice_name"),
            audio_encoding=request.get("audio_encoding", "LINEAR16"),
        )

    @staticmethod
    def normalize_response(audio_content: bytes) -> SynthesisResponse:
        return SynthesisResponse(audio_content=audio_content)
