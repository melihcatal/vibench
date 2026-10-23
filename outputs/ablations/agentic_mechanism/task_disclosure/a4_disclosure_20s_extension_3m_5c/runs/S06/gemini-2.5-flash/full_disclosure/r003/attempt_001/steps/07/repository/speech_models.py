
import dataclasses
from typing import Optional, Dict, Any

@dataclasses.dataclass
class SynthesizeRequest:
    text: str
    voice_id: str
    audio_config: Dict[str, Any] # e.g., {"audio_encoding": "LINEAR16", "sample_rate_hertz": 16000}

@dataclasses.dataclass
class SynthesizeResponse:
    audio_content: bytes
    metadata: Optional[Dict[str, Any]] = None

def normalize_text(text: str) -> str:
    """
    Performs basic text normalization for Text-to-Speech input.
    This is a placeholder and can be expanded with more sophisticated rules
    like number to word conversion, acronym expansion, etc.
    """
    # Example: basic whitespace and punctuation normalization
    normalized = text.strip()
    normalized = normalized.replace("  ", " ")
    # Add more normalization rules as needed
    return normalized
