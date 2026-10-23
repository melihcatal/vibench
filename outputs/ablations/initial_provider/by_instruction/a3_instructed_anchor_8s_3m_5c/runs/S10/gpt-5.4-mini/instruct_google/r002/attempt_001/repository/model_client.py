import os
from typing import Any, Dict, Optional


GOOGLE_GEMINI_MODEL = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.0-flash")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")


def default_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def google_generate_url(model: Optional[str] = None) -> str:
    return f"https://generativelanguage.googleapis.com/v1beta/models/{model or GOOGLE_GEMINI_MODEL}:generateContent"


def google_stream_url(model: Optional[str] = None) -> str:
    return f"https://generativelanguage.googleapis.com/v1beta/models/{model or GOOGLE_GEMINI_MODEL}:streamGenerateContent?alt=sse"


def auth_params() -> Dict[str, str]:
    if GOOGLE_API_KEY:
        return {"key": GOOGLE_API_KEY}
    return {}


def model_name(model: Optional[str] = None) -> str:
    return model or GOOGLE_GEMINI_MODEL
