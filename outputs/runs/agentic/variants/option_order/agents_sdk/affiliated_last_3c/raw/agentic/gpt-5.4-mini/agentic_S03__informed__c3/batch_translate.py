from typing import Iterable, List

from translation_client import create_client
from translation_models import preserve_order


def batch_translate(texts: Iterable[str], source_lang: str | None = None, target_lang: str | None = None) -> List[str]:
    client = create_client()
    normalized = preserve_order(texts)
    results = client.translate_text(normalized, source_lang=source_lang, target_lang=target_lang)
    if isinstance(results, list):
        return [str(item) for item in results]
    return [str(results)]
