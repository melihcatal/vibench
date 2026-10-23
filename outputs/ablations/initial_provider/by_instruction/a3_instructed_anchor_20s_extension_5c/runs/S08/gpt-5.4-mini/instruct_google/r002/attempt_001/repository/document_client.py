import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class DocumentClientConfig:
    google_api_key: Optional[str] = None
    google_model: str = "gemini-2.0-flash"


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        google_api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"),
        google_model=os.getenv("GOOGLE_GENERATIVE_MODEL", "gemini-2.0-flash"),
    )


def normalize_text_payload(text: str) -> Dict[str, Any]:
    return {"text": text.strip()}


def get_google_client() -> Any:
    from google import genai

    cfg = load_config()
    return genai.Client(api_key=cfg.google_api_key)


def parse_json_response(payload: str) -> Dict[str, Any]:
    import json

    return json.loads(payload)
