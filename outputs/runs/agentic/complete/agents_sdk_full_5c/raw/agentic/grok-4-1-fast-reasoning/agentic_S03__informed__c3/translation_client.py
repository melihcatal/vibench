import os
from typing import Optional

DEEPL_AUTH_KEY: Optional[str] = os.getenv("DEEPL_AUTH_KEY")

def ensure_deepl_configured() -> None:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")