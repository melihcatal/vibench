import typing as t

class TTSRequest:
    def __init__(self, text: str, voice: str = None, language: str = "en-US") -> None:
        self.text = text
        self.voice = voice
        self.language = language

    def as_dict(self) -> dict:
        """Convert request object to a dict suitable for Azure TTS SDK.

        Returns:
            dict: Payload representation.
        """
        payload = {"text": self.text}
        if self.voice:
            payload["voice_name"] = self.voice
        return payload


class TTSResponse:
    def __init__(self, audio_data: bytes, metadata: dict) -> None:
        self.audio_data = audio_data
        self.metadata = metadata

    @classmethod
    def from_raw_data(cls, data: dict) -> "TTSResponse":
        """Example parsing from Azure SDK raw result.

        Args:
            data (dict): Raw SDK response dict.

        Returns:
            TTSResponse: Parsed response.
        """
        return cls(audio_data=data["audio_data"], metadata=data["metadata"])

class VoiceCatalog:
    def __init__(self, service: str, locale: str) -> None:
        self.service = service
        self.locale = locale
        self.voices: t.List[str] = []

    def refresh(self) -> None:
        """Populate the list of available voice names for the service/locale.

        Raises:
            NotImplementedError: Must be implemented by subclasses per provider.
        """
        raise NotImplementedError("Subclasses must implement this")

# Minimal concrete implementation for Azure (kept for reference)
class AzureVoiceCatalog(VoiceCatalog):
    def refresh(self) -> None:
        from azure.cognitiveservices.speech import SpeechConfig
        cfg = SpeechConfig(subscription=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_SPEECH_REGION"))
        voices = cfg.get_voices()  # pseudo-code; Azure SDK does not expose this directly
        self.voices = [v["name"] for v in voices]

# Helper to pick a default voice
DEFAULT_VOICES = {
    "en-US": "en-US-JennyNeural",
    "en-GB": "en-GB_KateV3Voice",
    "es-ES": "es-ES_LauraV3Voice",
    "fr-FR": "fr-FR_ReneeV3Voice",
}

def get_default_voice(locale: str) -> str:
    """Return a safe default voice name for a given locale.

    Args:
        locale (str): BCP-47 language tag.

    Returns:
        str: Voice identifier string.
    """
        return DEFAULT_VOICES.get(locale, "en-US-JennyNeural")
