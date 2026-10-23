from __future__ import annotations

import os
from typing import Dict

from deepl import DeepLClient


DEEPL_TARGET_LANG_DEFAULT = "EN-US"


def translate_fields(fields: Dict[str, str], target_lang: str = DEEPL_TARGET_LANG_DEFAULT) -> Dict[str, str]:
    client = DeepLClient(os.environ["DEEPL_AUTH_KEY"])
    translated: Dict[str, str] = {}
    for key, value in fields.items():
        result = client.translate_text(value, target_lang=target_lang)
        translated[key] = result.text
    return translated
