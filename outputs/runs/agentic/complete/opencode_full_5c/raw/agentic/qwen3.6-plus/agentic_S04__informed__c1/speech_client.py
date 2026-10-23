import os
from dataclasses import dataclass, field
from typing import Optional

ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


@dataclass
class AssemblyAIConfig:
    api_key: str = field(
        default_factory=lambda: os.environ.get("ASSEMBLYAI_API_KEY", "")
    )
    api_base: str = ASSEMBLYAI_API_BASE
    poll_interval_seconds: float = 3.0
    max_poll_attempts: int = 200
    language_code: str = "en"
    enable_diarization: bool = False
    speaker_count: Optional[int] = None
    enable_word_timestamps: bool = True
    punctuate: bool = True
    format_text: bool = True
    dual_channel: bool = False

    def headers(self) -> dict:
        return {
            "authorization": self.api_key,
            "content-type": "application/json",
        }

    def is_valid(self) -> bool:
        return bool(self.api_key)


def load_config(
    api_key: Optional[str] = None,
    poll_interval_seconds: Optional[float] = None,
    max_poll_attempts: Optional[int] = None,
    language_code: Optional[str] = None,
    enable_diarization: Optional[bool] = None,
    speaker_count: Optional[int] = None,
) -> AssemblyAIConfig:
    config = AssemblyAIConfig()
    if api_key is not None:
        config.api_key = api_key
    if poll_interval_seconds is not None:
        config.poll_interval_seconds = poll_interval_seconds
    if max_poll_attempts is not None:
        config.max_poll_attempts = max_poll_attempts
    if language_code is not None:
        config.language_code = language_code
    if enable_diarization is not None:
        config.enable_diarization = enable_diarization
    if speaker_count is not None:
        config.speaker_count = speaker_count
    return config
