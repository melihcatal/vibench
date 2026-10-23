# [HELPER] speech_models.py
# Local request, response, and normalization helpers for Text-to-Speech
from typing import Dict, Any, Optional
from dataclasses import dataclass


# Minimal SSML wrapper
@dataclass
class SSMLRequest:
    text: str
    voice_name: Optional[str] = None
    pitch: Optional[str] = None  # e.g., "+10%"
    rate: Optional[str] = None  # e.g., "-20%"

    def to_ssml(self) -> str:
        parts = [f"<speak version='1.0' xml:lang='en-US'>"]
        if self.voice_name:
            parts.append(f"<voice name='{self.voice_name}'>")
        if self.pitch:
            parts.append(f"<prosody pitch='{self.pitch}'>")
        else:
            parts.append("<prosody>")
        parts.append(self.text)
        if self.pitch:
            parts.append("</prosody>")
        else:
            parts.append("</prosody>")
        if self.voice_name:
            parts.append("</voice>")
        parts.append("</speak>")
        return "".join(parts)


# Normalized TTS response across providers (currently Azure only)
@dataclass
class TTSResponse:
    audio_bytes: bytes
    duration_ms: int = 0  # optional, can be filled by provider-specific logic

    @classmethod
    def from_azure(cls, result) -> "TTSResponse":
        if result.reason != result.reasons_success:
            raise ValueError("Azure result not successful")
        return cls(
            audio_bytes=result.audio_data,
            duration_ms=result.duration_ms if hasattr(result, "duration_ms") else 0,
        )


# Helper to normalize provider responses to TTSResponse


def normalize_response(provider: str, raw) -> TTSResponse:
    if provider == "azure":
        return TTSResponse.from_azure(raw)
    raise NotImplementedError(f"Normalization for provider {provider} not implemented")
