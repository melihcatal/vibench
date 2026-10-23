from pydantic import BaseModel

class SSMLVoiceConfig(BaseModel):
    """
    Configuration for SSML voice synthesis.
    """
    language_code: str
    voice_name: str
    speaking_rate: float = 1.0
    pitch: float = 0.0

def normalize_ssml(ssml: str) -> str:
    """
    Normalizes SSML input for consistent processing.
    """
    return ssml.strip()