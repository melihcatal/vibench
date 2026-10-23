from typing import Dict, Any


class SynthesisRequest:
    """Container for normalized parameters passed to synthesis functions.

    Attributes:
        text (str): Plain text.
        ssml (str): SSML markup.
        voice_name (str): Voice identifier.
        audio_encoding (str): Desired encoding.
        prosody (dict): Optional prosody tweaks (rate, pitch, etc.).
    """

    def __init__(
        self,
        text: str = None,
        ssml: str = None,
        voice_name: str = None,
        audio_encoding: str = "MP3",
        prosody: Dict[str, float] = None,
    ):
        self.text = text
        self.ssml = ssml
        self.voice_name = voice_name
        self.audio_encoding = audio_encoding
        self.prosody = prosody or {}

    def to_google_input(self) -> Any:
        """Converts the generic request into a google.cloud.texttospeech SynthesisInput.
        Supports either plain text or SSML, not both.
        """
        module = __import__("google.cloud.texttospeech")
        if self.ssml:
            return module.SynthesisInput(ssml=self.ssml)
        else:
            return module.SynthesisInput(text=self.text)

    def to_google_audio_config(self) -> Any:
        """Builds an AudioConfig for the Google client."""
        module = __import__("google.cloud.texttospeech")
        return module.AudioConfig(audio_encoding=self.audio_encoding)

    def get_voice_name(self) -> str:
        return self.voice_name or "en-US-Wavenet-D"  # default fallback
