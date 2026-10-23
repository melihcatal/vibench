from dataclasses import dataclass


@dataclass
class VoiceSelectionParams:
    """Parameters for selecting a text-to-speech voice."""

    language_code: str
    name: str = None
    ssml_gender: str = None


@dataclass
class SynthesisRequest:
    """A request to synthesize speech."""

    text: str
    voice_params: VoiceSelectionParams
    output_encoding: str = "MP3"
