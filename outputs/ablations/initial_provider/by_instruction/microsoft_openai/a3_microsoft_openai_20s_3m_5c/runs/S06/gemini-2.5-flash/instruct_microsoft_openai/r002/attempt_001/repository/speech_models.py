from dataclasses import dataclass

@dataclass
class SynthesisRequest:
    text: str | None = None
    ssml: str | None = None
    voice_name: str | None = None
    locale: str | None = None

@dataclass
class SynthesisResponse:
    audio_content: bytes
    audio_format: str = "audio/wav" # Example default format

def normalize_text_for_synthesis(text: str) -> str:
    """
    Performs basic normalization on text before synthesis (e.g., trimming whitespace).
    """
    return text.strip()

def normalize_ssml_for_synthesis(ssml: str) -> str:
    """
    Performs basic normalization on SSML before synthesis.
    """
    # Add more robust SSML validation/normalization here if needed
    return ssml.strip()
