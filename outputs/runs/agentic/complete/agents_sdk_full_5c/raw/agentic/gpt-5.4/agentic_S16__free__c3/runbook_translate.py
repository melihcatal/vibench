from __future__ import annotations

import os
from typing import Optional

from deepl import DeepLClient


DEEPL_MODEL_TYPE = "prefer_quality_optimized"


def translate_runbook_notes(text: str, target_lang: str, auth_key: Optional[str] = None, source_lang: Optional[str] = None) -> str:
    client = DeepLClient(auth_key or os.getenv("DEEPL_AUTH_KEY", ""))
    result = client.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
        model_type=DEEPL_MODEL_TYPE,
    )
    return result.text
