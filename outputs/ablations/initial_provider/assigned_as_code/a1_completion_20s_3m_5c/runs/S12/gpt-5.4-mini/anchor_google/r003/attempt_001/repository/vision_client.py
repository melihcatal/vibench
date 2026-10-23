import os
from dataclasses import dataclass


@dataclass
class VisionConfig:
    google_credentials: str | None = None
    max_labels: int = 10
    max_text_results: int = 10
    language_hints: tuple[str, ...] = ()


def load_config(config=None):
    config = config or {}
    return VisionConfig(
        google_credentials=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        max_labels=int(config.get("max_labels", 10)),
        max_text_results=int(config.get("max_text_results", 10)),
        language_hints=tuple(config.get("language_hints", ())),
    )
