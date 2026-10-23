from dataclasses import dataclass

@dataclass
class VoiceDetail:
    """A simplified representation of a TTS voice for local application use."""
    name: str
    language_code: str
    ssml_gender: str

    def __str__(self):
        return f"{self.name} ({self.language_code}, {self.ssml_gender})"
