from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if locale is None:
        return None
    return locale.replace("_", "-").strip()


@dataclass
class SpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    ssml: bool = False
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text, "ssml": self.ssml}
        if self.voice is not None:
            payload["voice"] = self.voice
        if self.locale is not None:
            payload["locale"] = normalize_locale(self.locale)
        if self.speaking_rate is not None:
            payload["speaking_rate"] = self.speaking_rate
        if self.pitch is not None:
            payload["pitch"] = self.pitch
        return payload


@dataclass
class SpeechResponse:
    audio: bytes
    voice: Optional[str] = None
    locale: Optional[str] = None
