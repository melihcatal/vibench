from typing import Iterable, List

from translation_client import load_config, post_translate
from translation_models import normalize_text_list


def batch_translate(texts: Iterable[str], source_lang: str, target_lang: str) -> List[str]:
    items = normalize_text_list(texts)
    cfg = load_config()
    data = post_translate({"text": items, "source_lang": source_lang, "target_lang": target_lang}, cfg)
    return [item["text"] for item in data["translations"]]
