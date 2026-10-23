from dataclasses import dataclass
from typing import ByteString, Dict, Any

@dataclass
class SynthesizeRequest:
    """Normalization of incoming synthesis requests before dispatch to a concrete provider.
    
    Fields correspond to the most common parameters (providers differ slightly).
    """
    text: str = None
    ssml: str = None
    voice_name: str = "en-US-Wavenet-D"
    voice_locale: str = "en-US"
    audio_encoding: str = "MP3"
    audio_sample_rate: int = 24000
    # any additional provider‑specific params can be stored in `metadata`
    metadata: Dict[str, Any] = None

@dataclass
class SynthesisResult:
    """Container for response data returned from a provider.
    
    - `audio_content`: binary audio bytes
    - `metadata`: raw provider‑specific metadata (e.g., utterance stats, alignment)
    """
    audio_content: ByteString
    metadata: Dict[str, Any]

@dataclass
class VoiceInfo:
    """Summary of a voice returned by a provider.
    
    Typical fields: name, language_codes, gender, natural_sample_rate_Hz, type (STANDARD/NEURAL)
    """
    name: str
    language_codes: list[str]
    gender: str  # e.g., "FEMALE"/"MALE"
    natural_sample_rate_Hz: int
    type: str

@dataclass
class AudioConfig:
    """Common configuration for audio rendering across providers.
    
    Aligns with Google TTS and can be mapped to Azure, AWS, etc. as needed.
    """
    encoding: str
    sample_rate_hertz: int
    speaking_rate: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0
    silence_duration: float = 0.0
    # Provider‑specific extensions can be added as `metadata`
    metadata: Dict[str, Any] = None
