from dataclasses import dataclass
from typing import Optional, BinaryIO, List, Dict, Any

@dataclass
class SynthesisRequest:
    text: str
    text_type: str = "text"
    voice_id: str = "Joanna"
    output_format: str = "mp3"
    language_code: Optional[str] = None

@dataclass
class SynthesisResponse:
    audio_stream: BinaryIO
    content_type: str = "audio/mpeg"

@dataclass
class Voice:
    id: str
    name: str
    gender: str
    language_code: str
    supported_marks: List[str]
    supported_features: List[str]

def normalize_aws_voice_response(aws_voices: List[Dict[str, Any]]) -> List[Voice]:
    """
    Normalizes AWS Polly voice response to a common Voice model.
    """
    normalized_voices = []
    for v in aws_voices:
        normalized_voices.append(
            Voice(
                id=v["Id"],
                name=v["Name"],
                gender=v["Gender"],
                language_code=v["LanguageCode"],
                supported_marks=v.get("SupportedAudioFormats", []),
                supported_features=v.get("SupportedAudioFormats", []),
            )
        )
    return normalized_voices
