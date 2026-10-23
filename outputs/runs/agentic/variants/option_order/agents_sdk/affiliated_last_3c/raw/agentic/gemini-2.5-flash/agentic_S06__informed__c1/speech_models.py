from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class SynthesisRequest:
    """
    Represents a request for text-to-speech synthesis.
    """
    text: Optional[str] = None
    ssml: Optional[str] = None
    voice_name: str = "en-US-Wavenet-D"
    language_code: str = "en-US"
    audio_encoding: str = "MP3" # e.g., "MP3", "LINEAR16"
    speaking_rate: float = 1.0
    pitch: float = 0.0

    def __post_init__(self):
        if self.text is None and self.ssml is None:
            raise ValueError("Either 'text' or 'ssml' must be provided.")
        if self.text is not None and self.ssml is not None:
            raise ValueError("Cannot provide both 'text' and 'ssml'.")

@dataclass
class SynthesisResponse:
    """
    Represents the response from a text-to-speech synthesis.
    """
    audio_content: bytes
    audio_encoding: str = "MP3"

@dataclass
class Voice:
    """
    Represents a single available voice for text-to-speech.
    """
    name: str
    language_codes: List[str]
    ssml_gender: str # e.g., "MALE", "FEMALE", "NEUTRAL"
    natural_sample_rate_hertz: int

@dataclass
class VoiceSelection:
    """
    Represents parameters for selecting a specific voice.
    """
    language_code: str
    name: Optional[str] = None
    ssml_gender: Optional[str] = None # "MALE", "FEMALE", "NEUTRAL"

if __name__ == '__main__':
    # Example usage of the data models
    try:
        # Valid request with text
        req_text = SynthesisRequest(text="Hello from speech models!")
        print(f"Text Request: {req_text}")

        # Valid request with SSML
        req_ssml = SynthesisRequest(ssml="<speak>Hello from <emphasis>SSML</emphasis>!</speak>", speaking_rate=0.9)
        print(f"SSML Request: {req_ssml}")

        # Invalid request (missing text/ssml)
        # req_invalid = SynthesisRequest() # This would raise ValueError

        # Invalid request (both text and ssml)
        # req_invalid_both = SynthesisRequest(text="Hi", ssml="<speak>Hi</speak>") # This would raise ValueError

        # Voice example
        voice_example = Voice(
            name="en-US-Wavenet-F",
            language_codes=["en-US"],
            ssml_gender="FEMALE",
            natural_sample_rate_hertz=24000
        )
        print(f"Voice Example: {voice_example}")

    except ValueError as e:
        print(f"Error creating SynthesisRequest: {e}")
