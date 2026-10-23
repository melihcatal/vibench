from dataclasses import dataclass

@dataclass
class SynthesisRequest:
    text: str | None = None
    ssml: str | None = None
    voice_name: str | None = None
    locale: str = "en-US"
    output_format: str = "wav"

@dataclass
class SynthesisResponse:
    audio_content: bytes
    content_type: str = "audio/wav"

@dataclass
class Voice:
    name: str
    display_name: str
    locale: str
    gender: str
    voice_type: str

def normalize_text_for_synthesis(text: str) -> str:
    """
    Basic text normalization (e.g., trimming whitespace).
    """
    return text.strip()

def normalize_ssml_for_synthesis(ssml: str) -> str:
    """
    Basic SSML normalization (e.g., ensuring valid XML structure - highly simplified for this example).
    In a real scenario, a more robust XML parser/validator would be used.
    """
    # A very basic check to ensure it starts and ends with <speak>
    if not ssml.strip().startswith("<speak>"):
        ssml = f"<speak>{ssml}</speak>"
    if not ssml.strip().endswith("</speak>"):
        ssml = f"{ssml}</speak>"
    return ssml
