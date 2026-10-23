import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class SafetyConfig:
    google_api_key: Optional[str] = None
    google_model: str = "gemini-1.5-flash"
    google_base_url: str = "https://generativelanguage.googleapis.com"


def load_safety_config() -> SafetyConfig:
    return SafetyConfig(
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        google_model=os.getenv("GOOGLE_MODEL", "gemini-1.5-flash"),
        google_base_url=os.getenv("GOOGLE_BASE_URL", "https://generativelanguage.googleapis.com"),
    )


def google_headers(api_key: Optional[str] = None) -> dict:
    key = api_key or os.getenv("GOOGLE_API_KEY", "")
    return {"Content-Type": "application/json", "x-goog-api-key": key}
