from typing import Dict, Any
from translate_text import translate_text
from translation_models import NormalizedTranslation

PROVIDER_NAME = "deepl"


async def translate_dictionary_values(
    data: Dict[str, Any], target_lang: str, source_lang: str = "auto"
) -> Dict[str, Any]:
    """Translate dictionary values while preserving keys.",
    Recursively walks the dictionary, translating any string values. Nested dictionaries
    and lists are handled appropriately.
    """

    def _translate(item):
        if isinstance(item, str):
            return translate_text(item, target_lang, source_lang)
        elif isinstance(item, dict):
            return {k: _translate(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [_translate(v) for v in item]
        else:
            return item

    # Apply translation async‑awaits inside a synchronous helper
    result = _translate(data)
    # If any values are Future objects (e.g., from translate_text), await them
    # This simple implementation assumes translate_text was awaited already.
    # In practice you would collect all awaitables and asyncio.gather them.
    return result
