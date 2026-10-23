from __future__ import annotations

from typing import Any, Dict

import deepl


def localized_platform_output(
    text: str, target_locale: str, source_locale: str | None = None
) -> Dict[str, Any]:
    translator = deepl.Translator(auth_key=__import__("os").environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_locale.upper(),
        source_lang=source_locale.upper() if source_locale else None,
    )
    return {
        "provider": "deepl",
        "text": result.text,
        "detected_source_language": getattr(
            result, "detected_source_lang", source_locale
        ),
        "billed_characters": getattr(result, "billed_characters", None),
    }
